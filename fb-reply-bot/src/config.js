'use strict';

require('dotenv').config();

function optional(name, fallback = '') {
  const v = process.env[name];
  return v === undefined || v === '' ? fallback : v;
}

const config = {
  nodeEnv: optional('NODE_ENV', 'development'),

  fb: {
    pageAccessToken: optional('FB_PAGE_ACCESS_TOKEN'),
    pageId: optional('FB_PAGE_ID'),
    graphVersion: optional('FB_GRAPH_VERSION', 'v20.0'),
  },

  llm: {
    provider: optional('LLM_PROVIDER', 'anthropic').toLowerCase(),
    anthropic: {
      apiKey: optional('ANTHROPIC_API_KEY'),
      model: optional('ANTHROPIC_MODEL', 'claude-sonnet-4-6'),
    },
    openai: {
      apiKey: optional('OPENAI_API_KEY'),
      model: optional('OPENAI_MODEL', 'gpt-4o-mini'),
    },
  },

  bot: {
    persona: optional(
      'BOT_PERSONA',
      '你是一個親切、專業的粉專小編，用繁體中文簡短回覆，必要時引導客戶私訊詳談。'
    ),
    maxReplyChars: parseInt(optional('MAX_REPLY_CHARS', '280'), 10),
    replyKeywords: optional('REPLY_KEYWORDS', '')
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean),
  },

  poller: {
    intervalMinutes: parseInt(optional('INTERVAL_MINUTES', '60'), 10),
    lookbackHours: parseInt(optional('LOOKBACK_HOURS', '24'), 10),
    postLimit: parseInt(optional('POST_LIMIT', '10'), 10),
    conversationLimit: parseInt(optional('CONVERSATION_LIMIT', '20'), 10),
  },
};

module.exports = config;
