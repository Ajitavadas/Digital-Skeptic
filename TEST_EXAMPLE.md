# Test Example - Digital Skeptic AI

## Testing the Tool

Here's how to test the Digital Skeptic AI with a real news article:

### Sample Command
```bash
python main.py "https://www.bbc.com/news/technology-63533347" --output test_analysis.md
```

### Expected Workflow

1. **Article Extraction**
   ```
   [DIGITAL SKEPTIC] Initializing Digital Skeptic AI...
   [DIGITAL SKEPTIC] Extracting content from: https://www.bbc.com/news/technology-63533347

   ============================================================
   ARTICLE INFORMATION
   ============================================================
   Title: Twitter staff told to work long hours or leave
   Author(s): James Clayton
   URL: https://www.bbc.com/news/technology-63533347
   Content Length: 2847 characters
   Extraction Method: newspaper3k
   ============================================================
   ```

2. **AI Analysis Process**
   ```
   [DIGITAL SKEPTIC] Performing critical analysis...
   [DIGITAL SKEPTIC] Generating analysis report...
   [SUCCESS] Critical analysis report saved to: test_analysis.md
   ```

3. **Generated Report Structure**
   The tool will create a comprehensive markdown report with:
   - Article metadata and timestamp
   - Core claims extraction
   - Language and tone analysis
   - Potential red flags identification
   - Verification questions
   - Entity investigation guide
   - Alternative perspective
   - Usage instructions

### Sample Output Quality

The AI analysis is designed to provide insights like:

**Core Claims Example:**
• Elon Musk gave Twitter employees an ultimatum to commit to "hardcore" work
• Employees were given until 5pm Thursday to respond to the ultimatum
• Those who don't agree will receive three months of severance pay

**Language Analysis Example:**
"The article maintains a largely neutral, reportorial tone while covering a controversial workplace decision. The language is factual and measured, using direct quotes and attributed sources. However, the choice to highlight dramatic elements like 'ultimatum' and 'hardcore' in the headline and lead may amplify the confrontational nature of the story."

**Red Flags Example:**
• Relies heavily on anonymous employee sources for internal details
• Limited perspective from Twitter/company management beyond public statements
• Emotional impact of employee reactions emphasized over business rationale

### Advanced Features in Action

The tool's standout features provide additional value:

1. **Entity Recognition**: Identifies key players like Elon Musk, Twitter executives, and employee groups with specific investigation suggestions

2. **Counter-Perspective**: Presents alternative viewpoints like how the decision might be viewed as necessary business restructuring rather than hostile management

3. **Verification Questions**: Generates specific, actionable questions like "What is the legal precedent for such ultimatums in employment law?" and "How do other major tech companies handle similar restructuring situations?"

### Testing Different Article Types

Try the tool with various types of articles to see how it adapts:

```bash
# Political news
python main.py "https://www.reuters.com/world/us/..." --output political_analysis.md

# Business news  
python main.py "https://www.wsj.com/articles/..." --output business_analysis.md

# Science news
python main.py "https://www.nature.com/articles/..." --output science_analysis.md
```

Each article type will receive tailored analysis appropriate to its domain and typical bias patterns.
