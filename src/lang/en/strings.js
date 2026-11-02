// Тексты интерфейса, которые собирает код, — у каждого языка свои. {x} — подстановки; pl — формы слова по числу (Intl.PluralRules)
const T = {
  mixName: 'Mix', mixEp: 'Singularity', mixTitle: '{tech} for {domain}',
  badLink: 'No such idea — the link is out of date',
  stack: 'Stack', format: 'Format', trajectory: 'Path to prototype', anomaly: 'Anomaly', mdSteps: 'MVP steps',
  colon: ': ', sentSep: ' ', latinGap: false,   // двоеточие после подписи, разделитель предложений «Микса», пробел у латиницы в заголовке «Микса»
  again: '↻ Find another', copy: '⧉ Copy', fav: '✧ Add to constellation', faved: '✦ In constellation', share: '⤴ Share',
  askLabel: 'Analyze with AI:', askTitle: 'Opens {name} with this idea', askGoogle: 'AI Mode in Google (Gemini)',
  askPrompt: 'Review this AI project idea: “{title}”. {desc} Proposed stack: {stack}.{twist} Assess whether one or two developers can realistically build a prototype, what ready-made solutions and alternatives exist, the main risks, and where to start.',
  askTwist: ' Extra challenge: {twist}.',
  shareText: '{title} — an idea from AI_Rulet', linkCopied: 'Link copied', ideaCopied: 'Idea copied', copyFailed: 'Couldn’t copy',
  favAdded: 'Added to the constellation',
  emptyHistory: 'The chronicle is empty — no idea has arrived yet.', emptyFavs: 'The constellation is empty. Mark ideas with the star ✧.',
  remove: 'Remove', removeFav: 'Remove from the constellation', clearHistory: 'Clear the chronicle', exportMd: 'Export to .md',
  mdTitle: 'AI_Rulet — Constellation of ideas', mdFile: 'AI_Rulet-constellation.md',
  hintKeys: 'You can also press Space or Enter', hintEmpty: 'Space is empty — select at least one area',
  footer: '{ideas} in the catalog · {left} of {total} not drawn yet · {combos} in the Mix',
  soundOn: 'Sound on', soundOff: 'Sound off',
  noise: 'abcdefghijklmnopqrstuvwxyz0123456789◇◆✦⋆∴≈≡░▒',   // знаки помех в «Расшифровке сигнала»
  constNames: ['Neuron', 'Perceptron', 'Transformer', 'Gradient', 'Tensor', 'Embedding', 'Attention', 'Diffusion',
    'Token', 'Encoder', 'Decoder', 'Convolution', 'Agent', 'Latent space', 'Backpropagation', 'Random forest'],
  groupFrom: 1000,   // с какого числа разбивать разряды: по-английски 1,536
  pl: {
    idea: { one: 'idea', other: 'ideas' },
    combo: { one: 'combination', other: 'combinations' },
    areaIn: { one: 'area', other: 'areas' }
  }
};
