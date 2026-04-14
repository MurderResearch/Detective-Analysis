'use strict';

const logger = require('../utils/logger');
const fb = require('../services/facebook');
const llm = require('../services/llm');
const state = require('../store/state');

/**
 * 處理一通 Messenger 對話的最新訊息。
 * conversation: { id, participants, messages:{ data:[{id,message,from,created_time}] } }
 * 回傳 'replied' | 'skipped' | 'error'
 */
async function handleConversation(conversation, pageId) {
  const messages = conversation.messages?.data || [];
  if (messages.length === 0) return 'skipped';

  // Graph API 預設 messages 由新到舊排序
  const latest = messages[0];
  if (!latest || !latest.id) return 'skipped';

  // 粉專最新是自己發的 → 已經回過了
  if (latest.from?.id === pageId) return 'skipped';

  if (state.has('dm', latest.id)) return 'skipped';

  const psid = latest.from?.id;
  const text = (latest.message || '').trim();
  if (!psid || !text) {
    state.mark('dm', latest.id);
    return 'skipped';
  }

  // 24 小時視窗檢查：超過就不能主動 RESPONSE，先跳過
  const ageMs = Date.now() - new Date(latest.created_time).getTime();
  if (ageMs > 24 * 60 * 60 * 1000) {
    logger.warn('dm outside 24h window, skip', { psid, ageMs });
    state.mark('dm', latest.id);
    return 'skipped';
  }

  try {
    const reply = await llm.generateReply({
      source: 'message',
      userText: text,
      userName: latest.from?.name,
    });
    if (!reply) return 'skipped';
    await fb.sendMessage(psid, reply);
    state.mark('dm', latest.id);
    logger.info('replied to dm', { psid, reply });
    return 'replied';
  } catch (err) {
    logger.error('handleConversation failed', err.response?.data || err.message);
    return 'error';
  }
}

module.exports = { handleConversation };
