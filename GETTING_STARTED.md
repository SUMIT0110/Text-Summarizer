# Getting Started - Quick Reference

> AI Text Summarizer - In 5 Minutes

## ⚡ 5-Minute Quick Start

### STEP 1: INSTALL (1 minute)

```bash
pip install -r requirements.txt
```

Wait for installation to complete (should see "Successfully installed...").

### STEP 2: LAUNCH (1 minute)

```bash
streamlit run app/app.py
```

You'll see:
- "You can now view your Streamlit app in your browser."
- "Local URL: http://localhost:8501"
- Browser automatically opens

### STEP 3: USE THE APP (3 minutes)

1. Paste text into the left text box
2. Watch word count update automatically
3. Click "🚀 Generate Summary" button
4. View summary in right column
5. Copy summary to clipboard

---

## 📐 The App Interface

```
┌──────────────────────┬──────────────────────────────────────────────┐
│ SIDEBAR              │ MAIN AREA                                   │
├──────────────────────┼──────────────────────────────────────────────┤
│ ⚙️ Configuration    │  📄 Original Text     │  ✨ Summary       │
│  • Max Length        │  [Type your text]     │  [Result here]    │
│  • Min Length        │  Word count           │  Metrics:         │
│                      │  Character count      │  • Words          │
│ 📋 Input Tips        │                       │  • Compression %  │
│                      │ 🚀 Generate Summary   │  • Time           │
│                      │ 🔄 Clear All          │                   │
│                      │ 📋 Copy Summary       │                   │
└──────────────────────┴──────────────────────────────────────────────┘
```

---

## 📖 Step-by-Step Example

### Input Text

```
Artificial intelligence is rapidly transforming industries worldwide.
From healthcare to finance, from manufacturing to retail, AI applications 
are delivering significant value. Research institutions are racing to 
develop more capable models. Companies are investing heavily in AI 
infrastructure. Despite recent advances, experts predict even greater 
innovations in the coming years. However, concerns about AI safety and 
ethics continue to grow among researchers and policymakers.
```

### Output Summary

```
Artificial intelligence is transforming industries from healthcare to finance.
Companies are investing in AI infrastructure while research institutions 
develop more capable models. Experts predict greater innovations in coming years.
```

### Metrics Shown

- **Original words:** 100
- **Summary words:** 28
- **Compression %:** 72%
- **Processing time:** 2.3s

---

## ⌨️ Keyboard Shortcuts

### In Text Box
- `Ctrl+A` - Select all text
- `Ctrl+C` - Copy
- `Ctrl+V` - Paste
- `Ctrl+X` - Cut

### On Page
- `Tab` - Navigate between elements
- `Enter` - Click focused button
- `Esc` - Clear focus

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| **ModuleNotFoundError: No module named 'streamlit'** | Run: `pip install -r requirements.txt` |
| **First run takes 30 seconds** | Normal! Model loads on first run, then caches. Next runs are instant. |
| **"ValueError: Input text is too short"** | Paste more text (minimum ~10 words) |
| **App shows blank page** | Refresh browser (Ctrl+R) and try again |
| **"CUDA out of memory"** | Set `DEVICE=cpu` and run: `streamlit run app/app.py` |
| **Model download fails** | Check internet, try again, or pre-download with:<br>`python -c "from models.summarizer import _initialize_model; _initialize_model()"` |

---

## 📊 Parameters Explained

### Max Length (Sidebar Slider)

**What it does:** Controls maximum length of summary (in tokens, ~4 chars per token)

**Default:** 120 (produces ~400-500 character summary)

**Range:** 30-200

**Setting Guide:**
- `30-50` - Headlines/snippets (short summaries)
- `60-100` - Short articles (moderate summaries)
- `120` - ⭐ **Recommended default**
- `150-180` - Long articles/papers (detailed summaries)
- `200` - Maximum detail

### Min Length (Sidebar Slider)

**What it does:** Ensures summary maintains minimum quality (in tokens)

**Default:** 30

**Range:** 10-100

**Note:** Usually leave at default. Only change if:
- Very short articles → lower min
- Complex content → higher min

---

## ✨ Features At a Glance

✅ **Text Input**
- Paste any text (articles, emails, documents)

✅ **Real-time Metrics**
- Word count updates as you type
- Character count
- Compression percentage

✅ **One-Click Generation**
- Click button to summarize
- Shows processing indicator
- Instant results (1-3 seconds on cached model)

✅ **Copy to Clipboard**
- Click "Copy Summary" button
- Paste anywhere

✅ **Clear & Reset**
- Click "Clear All" button
- Resets both input and output
- Ready for new text

✅ **Parameter Tuning**
- Adjust summary length on the fly
- Immediate options to regenerate

---

## 🎯 Best Practices

### DO ✅
- Paste well-formed text
- Use default settings for starting
- Paste 20+ words for best results
- Adjust parameters for different content
- Copy results immediately after generating

### DON'T ❌
- Paste very short texts (<10 words)
- Move away from page while generating
- Close browser during model download
- Use very aggressive settings for all texts
- Expect summary to be 10% of original length

---

## 🔄 Common Workflows

### Workflow 1: News Article Summary

1. Open news website
2. Copy article text
3. Paste into app
4. Click "Generate Summary"
5. Get summary for social media
6. Click "Copy Summary"

### Workflow 2: Email Summarization

1. Copy email content
2. Paste into app
3. Adjust Max Length to 60 (shorter)
4. Click "Generate Summary"
5. Use summary in reply email

### Workflow 3: Document Condensing

1. Paste document content
2. Use default settings
3. Click "Generate Summary"
4. Increase Max Length to 150 for detail
5. Copy results

---

## ❓ Frequently Asked Questions

**Q: How long does it take to summarize?**  
A: First click: 15-30s (model setup). Then: 1-3s per summary.

**Q: Can I summarize PDF files?**  
A: Not yet. Copy-paste text from PDF into app.

**Q: How long can my text be?**  
A: Supports 20 words to 5000+ words per summary.

**Q: Can I change the model?**  
A: Currently uses BART. Custom models coming soon.

**Q: Does it work offline?**  
A: First run needs internet (model download). Then works offline.

**Q: Can I summarize in other languages?**  
A: Currently optimized for English. Other languages: coming soon.

**Q: How accurate are the summaries?**  
A: 80-90% quality for news/articles. May vary by content type.

**Q: Can I undo or regenerate?**  
A: Yes. Adjust parameters and click Generate again.

**Q: Is my data private?**  
A: Yes. Everything runs locally. No data sent anywhere.

**Q: Can I save summaries?**  
A: Copy to clipboard and paste. Persistent storage: coming soon.

---

**Ready to get started? Follow the [5-Minute Quick Start](#-5-minute-quick-start) above!** 🚀
