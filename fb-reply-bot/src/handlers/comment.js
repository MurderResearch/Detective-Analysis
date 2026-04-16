'use strict';

const config = require('../config');
const logger = require('../utils/logger');
const fb = require('../services/facebook');
const llm = require('../services/llm');
const state = require('../store/state');

/**
 * 處理一則粉專貼文留言。
 * comment: { id, message, from:{id,name}, created_time, comment_count }
 * post:    { id, message }
 * 回傳 'replied' | 'skipped' | 'error'
 */
async function handleComment(comment, post, pageId) {
  const cid = comment.id;
  if (!cid) return 'skipped';

  // 自家粉專的留言不回
  if (comment.from && comment.from.id === pageId) {
    state.mark('comment', cid);
    return 'skipped';
  }

  if (state.has('comment', cid)) return 'skipped';

  // 若底下已經有粉專的回覆了，就標記略過
  if (comment.comment_count && comment.comment_count > 0) {
    try {
      const replies = await fb.listCommentReplies(cid);
      const pageReplied = replies.some((r) => r.from?.id === pageId);
      if (pageReplied) {
        state.mark('comment', cid);
        logger.debug('comment already replied by page, skip', { cid });
        return 'skipped';
      }
    } catch (err) {
      logger.warn('listCommentReplies failed', err.response?.data || err.message);
    }
  }

  const text = (comment.message || '').trim();
  if (!text) {
    state.mark('comment', cid);
    return 'skipped';
  }

  if (looksLikeInjection(text)) {
    logger.warn('prompt injection attempt detected, skip', { cid, text });
    state.mark('comment', cid);
    return 'skipped';
  }

  if (!matchesKeywords(text)) {
    logger.debug('keyword not matched, skip', { cid });
    state.mark('comment', cid);
    return 'skipped';
  }

  try {
    const reply = await llm.generateReply({
      source: 'comment',
      userText: text,
      postText: post?.message,
      userName: comment.from?.name,
    });
    if (!reply) return 'skipped';
    await fb.replyToComment(cid, reply);
    state.mark('comment', cid);
    logger.info('replied to comment', { cid, reply });
    return 'replied';
  } catch (err) {
    logger.error('handleComment failed', err.response?.data || err.message);
    return 'error';
  }
}

/**
 * 偵測明顯的 prompt injection 嘗試。
 * 符合任一模式就回傳 true，該留言會被跳過不回覆。
 */
function looksLikeInjection(text) {
  const lower = text.toLowerCase();
  const patterns = [
    // 中文 injection
    /忽略(以上|上面|之前|先前)(的|所有)?(指令|規則|設定|提示)/,
    /你現在是(一[隻個頭條])?/,
    /請?(用|以).{0,6}(語|腔|口吻|身份|角色)(回覆|回答|說話)/,
    /輸出(你的)?(system\s*prompt|系統提示|指令|設定)/,
    /貼出.{0,6}(token|key|密碼|密鑰|金鑰)/,
    /洩漏.{0,6}(token|key|api|密碼|設定)/,
    /扮演.{0,4}(角色|人物|機器人|助手)/,
    /從現在起你(是|要|必須)/,
    // 英文 injection
    /ignore\s+(all\s+)?(previous|above|prior)\s+(instructions?|rules?|prompts?)/i,
    /you\s+are\s+now\s+a/i,
    /repeat\s+(the\s+)?(above|system|your)\s*(prompt|instructions?|message)?/i,
    /output\s+(your\s+)?(system\s*prompt|instructions?|api\s*key|token)/i,
    /reveal\s+(your\s+)?(system|api|secret|token|key|prompt)/i,
    /pretend\s+(to\s+be|you\s+are)/i,
    /jailbreak/i,
    /DAN\s*mode/i,
    /do\s+anything\s+now/i,
  ];
  return patterns.some((p) => p.test(text));
}

function matchesKeywords(text) {
  const kws = config.bot.replyKeywords;
  if (!kws || kws.length === 0) return true;
  const lower = text.toLowerCase();
  return kws.some((k) => lower.includes(k.toLowerCase()));
}

module.exports = { handleComment };
