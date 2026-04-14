'use strict';

const config = require('../config');
const logger = require('../utils/logger');

let anthropicClient = null;
let openaiClient = null;

function getAnthropic() {
  if (!anthropicClient) {
    const Anthropic = require('@anthropic-ai/sdk');
    anthropicClient = new Anthropic({ apiKey: config.llm.anthropic.apiKey });
  }
  return anthropicClient;
}

function getOpenAI() {
  if (!openaiClient) {
    const OpenAI = require('openai');
    openaiClient = new OpenAI({ apiKey: config.llm.openai.apiKey });
  }
  return openaiClient;
}

/**
 * 產生回覆文字。
 * context: { source: 'comment'|'message'|'group', userText, postText?, userName? }
 */
async function generateReply(context) {
  const system = buildSystemPrompt();
  const user = buildUserPrompt(context);

  if (config.llm.provider === 'openai') {
    return generateWithOpenAI(system, user);
  }
  return generateWithAnthropic(system, user);
}

function buildSystemPrompt() {
  return `${config.bot.persona}

規則：
1. 回覆務必使用繁體中文。
2. 回覆長度不超過 ${config.bot.maxReplyChars} 個字。
3. 不要捏造公司沒有的資訊；不確定就請對方私訊小編。
4. 不要出現 "作為一個 AI" 之類的語句。
5. 若為敏感、投訴或醫療法律問題，請請對方私訊並表示會有真人處理。
`;
}

function buildUserPrompt(ctx) {
  const source = {
    comment: '粉專貼文留言',
    message: 'Messenger 私訊',
    group: '社團貼文/留言',
  }[ctx.source] || ctx.source;

  const lines = [`來源：${source}`];
  if (ctx.userName) lines.push(`使用者：${ctx.userName}`);
  if (ctx.postText) lines.push(`原始貼文：${ctx.postText}`);
  lines.push(`使用者訊息：${ctx.userText}`);
  lines.push('');
  lines.push('請直接輸出要回覆的文字，不要加引號或其他說明。');
  return lines.join('\n');
}

async function generateWithAnthropic(system, user) {
  const client = getAnthropic();
  const resp = await client.messages.create({
    model: config.llm.anthropic.model,
    max_tokens: 512,
    system,
    messages: [{ role: 'user', content: user }],
  });
  const text = (resp.content || [])
    .filter((b) => b.type === 'text')
    .map((b) => b.text)
    .join('\n')
    .trim();
  logger.debug('anthropic reply', { text });
  return truncate(text);
}

async function generateWithOpenAI(system, user) {
  const client = getOpenAI();
  const resp = await client.chat.completions.create({
    model: config.llm.openai.model,
    max_tokens: 512,
    messages: [
      { role: 'system', content: system },
      { role: 'user', content: user },
    ],
  });
  const text = resp.choices?.[0]?.message?.content?.trim() || '';
  logger.debug('openai reply', { text });
  return truncate(text);
}

function truncate(text) {
  const max = config.bot.maxReplyChars;
  if (text.length <= max) return text;
  return text.slice(0, max - 1) + '…';
}

module.exports = { generateReply };
