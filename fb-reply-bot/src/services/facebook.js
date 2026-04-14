'use strict';

const axios = require('axios');
const config = require('../config');
const logger = require('../utils/logger');

const GRAPH = `https://graph.facebook.com/${config.fb.graphVersion}`;
const PAGE_TOKEN = () => config.fb.pageAccessToken;

// ---------- 讀取 ----------

/**
 * 列出粉專最近的貼文（含留言摘要）。
 * since: 只抓這個 ISO 時間之後的貼文
 */
async function listRecentPosts({ limit = 10, since } = {}) {
  const url = `${GRAPH}/${config.fb.pageId}/posts`;
  const params = {
    fields:
      'id,message,created_time,comments.limit(50){id,message,from,created_time,comment_count,parent}',
    limit,
    access_token: PAGE_TOKEN(),
  };
  if (since) params.since = Math.floor(new Date(since).getTime() / 1000);

  const { data } = await axios.get(url, { params });
  return data.data || [];
}

/**
 * 拿單一留言底下的回覆。
 */
async function listCommentReplies(commentId) {
  const url = `${GRAPH}/${commentId}/comments`;
  const { data } = await axios.get(url, {
    params: {
      fields: 'id,message,from,created_time',
      limit: 50,
      access_token: PAGE_TOKEN(),
    },
  });
  return data.data || [];
}

/**
 * 列出粉專最近的 Messenger 對話（含最新幾則訊息）。
 */
async function listConversations({ limit = 20 } = {}) {
  const url = `${GRAPH}/${config.fb.pageId}/conversations`;
  const { data } = await axios.get(url, {
    params: {
      fields:
        'id,updated_time,participants,messages.limit(5){id,message,from,created_time}',
      limit,
      access_token: PAGE_TOKEN(),
    },
  });
  return data.data || [];
}

// ---------- 回覆 ----------

async function replyToComment(commentId, message) {
  const url = `${GRAPH}/${commentId}/comments`;
  const { data } = await axios.post(url, null, {
    params: { message, access_token: PAGE_TOKEN() },
  });
  logger.info('replyToComment ok', { commentId, newId: data.id });
  return data;
}

async function sendMessage(recipientPsid, text) {
  const url = `${GRAPH}/me/messages`;
  const body = {
    recipient: { id: recipientPsid },
    messaging_type: 'RESPONSE',
    message: { text },
  };
  const { data } = await axios.post(url, body, {
    params: { access_token: PAGE_TOKEN() },
  });
  logger.info('sendMessage ok', { recipientPsid });
  return data;
}

module.exports = {
  listRecentPosts,
  listCommentReplies,
  listConversations,
  replyToComment,
  sendMessage,
};
