'use strict';

const config = require('./config');
const logger = require('./utils/logger');
const fb = require('./services/facebook');
const state = require('./store/state');
const { handleComment } = require('./handlers/comment');
const { handleConversation } = require('./handlers/message');

/**
 * 執行一次 poll：
 *   1) 抓最近的粉專貼文 → 遍歷每則貼文的留言 → 未回覆就回
 *   2) 抓最近的 Messenger 對話 → 最新訊息是使用者發的就回
 * 結束時把 state 寫檔。
 *
 * 回傳 { comments:{replied,skipped,errors}, dms:{...} }
 */
async function runOnce() {
  const startedAt = new Date();
  logger.info('=== poll start ===', { at: startedAt.toISOString() });

  const stats = {
    comments: { replied: 0, skipped: 0, errors: 0 },
    dms: { replied: 0, skipped: 0, errors: 0 },
  };

  await pollComments(stats);
  await pollMessenger(stats);

  state.flush();
  const durMs = Date.now() - startedAt.getTime();
  logger.info('=== poll done ===', { durMs, ...stats });
  return stats;
}

async function pollComments(stats) {
  if (!config.fb.pageId || !config.fb.pageAccessToken) {
    logger.warn('skip pollComments: FB_PAGE_ID / FB_PAGE_ACCESS_TOKEN 未設定');
    return;
  }
  try {
    const sinceMs = Date.now() - config.poller.lookbackHours * 3600 * 1000;
    const posts = await fb.listRecentPosts({
      limit: config.poller.postLimit,
      since: new Date(sinceMs).toISOString(),
    });
    logger.info('fetched posts', { count: posts.length });

    for (const post of posts) {
      const comments = post.comments?.data || [];
      for (const c of comments) {
        // 只處理頂層留言，跳過某條留言底下的回覆
        if (c.parent && c.parent.id && c.parent.id !== post.id) continue;
        const r = await handleComment(c, post, config.fb.pageId);
        stats.comments[r === 'replied' ? 'replied' : r === 'error' ? 'errors' : 'skipped']++;
      }
    }
  } catch (err) {
    stats.comments.errors++;
    logger.error('pollComments failed', err.response?.data || err.message);
  }
}

async function pollMessenger(stats) {
  if (!config.fb.pageId || !config.fb.pageAccessToken) {
    logger.warn('skip pollMessenger: FB_PAGE_ID / FB_PAGE_ACCESS_TOKEN 未設定');
    return;
  }
  try {
    const conversations = await fb.listConversations({
      limit: config.poller.conversationLimit,
    });
    logger.info('fetched conversations', { count: conversations.length });

    for (const conv of conversations) {
      const r = await handleConversation(conv, config.fb.pageId);
      stats.dms[r === 'replied' ? 'replied' : r === 'error' ? 'errors' : 'skipped']++;
    }
  } catch (err) {
    stats.dms.errors++;
    logger.error('pollMessenger failed', err.response?.data || err.message);
  }
}

module.exports = { runOnce };
