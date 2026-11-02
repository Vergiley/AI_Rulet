// Тексты интерфейса, которые собирает код, — у каждого языка свои. {x} — подстановки; pl — формы слова по числу (Intl.PluralRules)
const T = {
  mixName: '混搭', mixEp: '奇点', mixTitle: '面向{domain}的{tech}',
  badLink: '没有这个创意——链接已过期',
  stack: '技术栈', format: '形式', trajectory: '原型路线', anomaly: '额外挑战', mdSteps: 'MVP 步骤',
  colon: '：', sentSep: '', latinGap: true,   // двоеточие после подписи, разделитель предложений «Микса», пробел у латиницы в заголовке «Микса»
  again: '↻ 再找一个', copy: '⧉ 复制', fav: '✧ 加入星图', faved: '✦ 已在星图中', share: '⤴ 分享',
  askLabel: '用 AI 分析：', askTitle: '在 {name} 中打开这个创意', askGoogle: 'Google AI 模式（Gemini）',
  askPrompt: '请分析这个 AI 项目创意：“{title}”。{desc}建议的技术栈：{stack}。{twist}请评估一到两名开发者能否做出原型、有哪些现成方案和替代品、主要风险是什么，以及应该从哪里入手。',
  askTwist: '额外挑战：{twist}。',
  shareText: '{title} —— 来自 AI_Rulet 的创意', linkCopied: '链接已复制', ideaCopied: '创意已复制', copyFailed: '复制失败',
  favAdded: '已加入星图',
  emptyHistory: '航行日志是空的——还没有创意飞来。', emptyFavs: '星图是空的。用 ✧ 标记喜欢的创意。',
  remove: '移除', removeFav: '从星图中移除', clearHistory: '清空航行日志', exportMd: '导出为 .md',
  mdTitle: 'AI_Rulet —— 创意星图', mdFile: 'AI_Rulet-星图.md',
  hintKeys: '也可以按空格键或 Enter 键', hintEmpty: '星空空空如也——请至少选择一个领域',
  footer: '目录中有 {ideas} · 尚未抽到 {left}/{total} · 混搭共有 {combos}',
  soundOn: '声音已开启', soundOff: '声音已关闭',
  noise: '的一是不了人我在有他这为之大来以个中上们到说国和地也子时道出而要于就下得可你年生0123456789◇◆✦⋆∴≈≡░▒',   // знаки помех в «Расшифровке сигнала»
  constNames: ['神经元', '感知机', 'Transformer', '梯度', '张量', '嵌入', '注意力', '扩散',
    '词元', '编码器', '解码器', '卷积', '智能体', '潜空间', '反向传播', '随机森林'],
  groupFrom: 10000,   // с какого числа разбивать разряды: 1536, но 3,072,735
  pl: {
    idea: { other: '个创意' },
    combo: { other: '种组合' },
    areaIn: { other: '个领域' }
  }
};
