#!/usr/bin/env node
'use strict';

/**
 * 只讀不寫的煙霧測試。
 * 驗證 FB_PAGE_ID + FB_PAGE_ACCESS_TOKEN + 權限是否正確。
 * 不呼叫 LLM、不做任何回覆。
 *
 * 用法：node scripts/test-read.js
 */

const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

const fb = require('../src/services/facebook');
const config = require('../src/config');

function dumpError(prefix, err) {
  console.error(prefix + '：');
  if (err.response) {
    console.error('  status    :', err.response.status);
    console.error('  statusText:', err.response.statusText);
    console.error('  url       :', err.config?.url);
    if (err.response.data) {
      console.error('  body      :', JSON.stringify(err.response.data, null, 2));
    } else {
      console.error('  (response body 為空)');
    }
  } else if (err.request) {
    console.error('  (沒有收到回應，網路問題?)');
    console.error('  url       :', err.config?.url);
  } else {
    console.error('  message   :', err.message);
  }
}

async function main() {
  console.log('=== fb-reply-bot read-only smoke test ===');
  console.log('Page ID       :', config.fb.pageId);
  console.log('Graph version :', config.fb.graphVersion);
  console.log('Token length  :', config.fb.pageAccessToken.length);
  console.log('');

  // 1) 粉專貼文 + 留言
  try {
    const posts = await fb.listRecentPosts({
      limit: 5,
      since: new Date(Date.now() - config.poller.lookbackHours * 3600 * 1000).toISOString(),
    });
    console.log(`✅ 粉專貼文 (${posts.length} 篇，最近 ${config.poller.lookbackHours} 小時內):`);
    for (const p of posts) {
      const msg = (p.message || '(無文字)').replace(/\s+/g, ' ').slice(0, 60);
      const comments = p.comments?.data || [];
      console.log(`  • [${p.id}] ${p.created_time}`);
      console.log(`    "${msg}"`);
      console.log(`    → ${comments.length} 則頂層留言`);
      for (const c of comments) {
        const cmsg = (c.message || '(無)').replace(/\s+/g, ' ').slice(0, 60);
        const who = c.from?.name || c.from?.id || '?';
        const self = c.from?.id === config.fb.pageId ? ' (粉專自己)' : '';
        console.log(`       - [${c.id}] @${who}${self}: "${cmsg}"`);
      }
    }
  } catch (err) {
    dumpError('❌ 讀取粉專貼文失敗', err);
    process.exitCode = 1;
  }

  console.log('');

  // 2) Messenger 對話
  try {
    const convs = await fb.listConversations({ limit: 5 });
    console.log(`✅ Messenger 對話 (${convs.length} 通):`);
    for (const c of convs) {
      const participants = (c.participants?.data || [])
        .map((p) => p.name || p.id)
        .join(', ');
      const msgs = c.messages?.data || [];
      console.log(`  • [${c.id}] ${participants}`);
      const latest = msgs[0];
      if (latest) {
        const who = latest.from?.name || '?';
        const text = (latest.message || '(附件/貼圖)').replace(/\s+/g, ' ').slice(0, 60);
        const self = latest.from?.id === config.fb.pageId ? ' (粉專自己回過)' : '';
        console.log(`    最新訊息 @${who}${self}: "${text}"  (${latest.created_time})`);
      } else {
        console.log('    (無訊息)');
      }
    }
  } catch (err) {
    dumpError('❌ 讀取 Messenger 對話失敗', err);
    process.exitCode = 1;
  }

  console.log('');
  console.log(process.exitCode ? '=== ❌ 測試有錯，請看上方訊息 ===' : '=== ✅ 讀取測試全部通過 ===');
}

main().catch((err) => {
  console.error('fatal:', err);
  process.exit(1);
});
