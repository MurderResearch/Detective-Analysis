'use strict';

const fs = require('fs');
const path = require('path');
const logger = require('../utils/logger');

/**
 * 極簡 state store：
 * 把「已回覆過的 ID」存成 JSON 檔，避免 polling 每小時重複回覆。
 * key 格式 "type:id"（例如 "comment:123_456"、"dm:m_xxx"）。
 * 每筆記錄一個 timestamp，可以用 TTL 清掉太舊的。
 */

const DEFAULT_PATH =
  process.env.STATE_FILE ||
  path.join(process.cwd(), '.fb-reply-bot-state.json');

const TTL_DAYS = parseInt(process.env.STATE_TTL_DAYS || '30', 10);
const TTL_MS = TTL_DAYS * 24 * 60 * 60 * 1000;

let store = null;
let filePath = DEFAULT_PATH;

function load() {
  if (store) return store;
  try {
    if (fs.existsSync(filePath)) {
      const raw = fs.readFileSync(filePath, 'utf8');
      store = JSON.parse(raw);
    } else {
      store = {};
    }
  } catch (err) {
    logger.warn('state load failed, starting empty', err.message);
    store = {};
  }
  prune();
  return store;
}

function save() {
  try {
    fs.writeFileSync(filePath, JSON.stringify(store, null, 2), 'utf8');
  } catch (err) {
    logger.error('state save failed', err.message);
  }
}

function prune() {
  if (!store) return;
  const cutoff = Date.now() - TTL_MS;
  let removed = 0;
  for (const k of Object.keys(store)) {
    if ((store[k] || 0) < cutoff) {
      delete store[k];
      removed++;
    }
  }
  if (removed > 0) logger.debug('state pruned', { removed });
}

function _key(type, id) {
  return `${type}:${id}`;
}

function has(type, id) {
  load();
  return Object.prototype.hasOwnProperty.call(store, _key(type, id));
}

function mark(type, id) {
  load();
  store[_key(type, id)] = Date.now();
}

function flush() {
  if (!store) return;
  save();
}

function setPath(p) {
  filePath = p;
  store = null;
}

module.exports = { has, mark, flush, setPath };
