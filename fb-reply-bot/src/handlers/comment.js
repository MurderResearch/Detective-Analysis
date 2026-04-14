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

function matchesKeywords(text) {
  const kws = config.bot.replyKeywords;
  if (!kws || kws.length === 0) return true;
  const lower = text.toLowerCase();
  return kws.some((k) => lower.includes(k.toLowerCase()));
}

module.exports = { handleComment };
