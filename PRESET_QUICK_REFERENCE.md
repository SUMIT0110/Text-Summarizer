# Quick Reference: Summary Length Presets

## 🎯 Preset Quick Start

### Select Your Preset
Open the app sidebar and choose:

| Option | When to Use | Output Size |
|--------|------------|------------|
| **Short 🎯** | Headlines, news, quick facts | ~150-250 chars |
| **Medium ⚖️** | Articles, emails, reports | ~400-500 chars |
| **Long 📚** | Research, detailed summaries | ~700-900 chars |

## 📋 Three Steps to Summarize

1. **Paste text** → Enter text to summarize
2. **Pick preset** → Select Short, Medium, or Long
3. **Generate** → Click "🚀 Generate Summary"

## 🔧 Power User: Custom Settings

Need finer control?

1. Open "⚙️ Advanced Parameters" section
2. Click "🔧 Customize Settings" expander
3. Adjust sliders:
   - **Max Length**: 30-200 tokens
   - **Min Length**: 10-100 tokens
4. Generate summary with custom values

## ⚡ Tips

✓ **Default is Medium** - Works for most texts
✓ **Short for quick reads** - Headlines and snippets
✓ **Long for details** - Full information required
✓ **Minimum 10 words** - Too short texts won't work
✓ **Same model always** - Only length changes, quality consistent

## 🎓 Understanding the Options

**Short 🎯 (60 tokens)**
- Best for: News briefs, social media
- Example: "AI transforms industries fast"
- Compression: 80-90% reduction

**Medium ⚖️ (120 tokens)**
- Best for: General use, default choice
- Example: "AI is revolutionizing sectors through automation, with applications in healthcare, finance, and manufacturing"
- Compression: 60-70% reduction

**Long 📚 (200 tokens)**
- Best for: Academic, comprehensive
- Example: "AI transforms multiple sectors through automation and intelligence. Healthcare uses it for diagnosis and treatment planning. Finance applies it for risk assessment and trading. Manufacturing optimizes production. Each sector benefits differently but faces similar challenges with implementation and ethics."
- Compression: 40-50% reduction

## ⚙️ What Do These Numbers Mean?

- **Tokens**: Model's measurement unit (~4-5 characters per token)
- **Max Length**: Summary won't exceed this length
- **Min Length**: Summary must be at least this long
- **Compression**: % of original text that was removed

## 🚀 Running the App

```bash
cd ai-text-summarizer
streamlit run app/app.py
```

## 📊 Example Session

**Input Text** (245 words):
```
Artificial intelligence is transforming industries...
[Full article text here]
```

**Short 🎯 Output** (~160 chars):
```
AI is revolutionizing multiple sectors through
automation and intelligence applications.
```

**Medium ⚖️ Output** (~450 chars):
```
AI is revolutionizing sectors through automation
and specialized intelligence. Healthcare uses it 
for diagnosis and treatment planning. Finance applies 
it for risk assessment. Manufacturing optimizes 
production. Each sector faces implementation challenges.
```

**Long 📚 Output** (~850 chars):
```
AI is transforming multiple sectors through
automation and intelligent systems. In healthcare,
it enables precise diagnosis and treatment planning.
Finance leverages it for comprehensive risk assessment
and algorithmic trading. Manufacturing uses it to
optimize production processes and quality control.
Education personalizes learning experiences. Retail
enhances customer experience and inventory management.
Despite significant benefits, implementation faces
challenges including data quality, skilled personnel,
integration complexity, and ethical concerns about
bias and transparency.
```

## ❓ Common Issues

**Q: Summary is too short**
A: Try Medium or Long preset, or increase max_length in custom settings

**Q: Summary isn't detailed enough**
A: Switch to Long preset or customize advanced parameters

**Q: Text is rejected as too short**
A: Minimum 10 words required; aim for 50+ words for best results

**Q: Generator is slow**
A: Long texts take longer (5-10 seconds); short texts are faster (2-3 seconds)

**Q: Same text, different summaries**
A: Model uses deterministic beam search (same input = same output); clear browser cache if experiencing issues

## 🎯 Best Practices

✅ **DO:**
- Paste well-structured text
- Try Medium first, then adjust
- Use Short for quick reads
- Use Long for comprehensive summaries
- Let the text have clear topic

❌ **DON'T:**
- Use text shorter than 10 words
- Expect perfect technical accuracy
- Use lists without context
- Paste multiple unrelated texts together
- Use for code or programming documentation

## 📞 Need Help?

See **ENHANCEMENT_GUIDE.md** for detailed documentation
See **GETTING_STARTED.py** for setup instructions

---

**Remember**: Choose the preset that matches your needs, then click Generate. It's that simple! 🚀
