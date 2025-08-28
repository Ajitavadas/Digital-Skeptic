import openai
from typing import Dict, List, Optional
import json
import re
from config import Config


class AIAnalysisError(Exception):
    """Custom exception for AI analysis errors."""
    pass


class DigitalSkepticAnalyzer:
    """
    Sophisticated AI analyzer that performs critical analysis of news articles.
    Uses advanced prompt engineering to generate insightful, nuanced analysis.
    """

    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required")

        openai.api_key = Config.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

    def analyze_article(self, article_data: Dict[str, str]) -> Dict[str, any]:
        """
        Perform comprehensive critical analysis of the article.

        Args:
            article_data (Dict[str, str]): Article content and metadata

        Returns:
            Dict[str, any]: Complete analysis results
        """
        try:
            # Core analysis
            core_claims = self._extract_core_claims(article_data)
            language_analysis = self._analyze_language_and_tone(article_data)
            red_flags = self._identify_red_flags(article_data)
            verification_questions = self._generate_verification_questions(article_data)

            # Stand-out features
            entities = self._perform_entity_recognition(article_data)
            counter_argument = self._generate_counter_argument(article_data)

            return {
                'core_claims': core_claims,
                'language_analysis': language_analysis,
                'red_flags': red_flags,
                'verification_questions': verification_questions,
                'entities': entities,
                'counter_argument': counter_argument,
                'article_metadata': {
                    'title': article_data.get('title', 'Unknown Title'),
                    'url': article_data.get('url', ''),
                    'authors': article_data.get('authors', 'Unknown Author'),
                    'publish_date': article_data.get('publish_date', 'Unknown Date')
                }
            }

        except Exception as e:
            raise AIAnalysisError(f"Analysis failed: {str(e)}")

    def _extract_core_claims(self, article_data: Dict[str, str]) -> List[str]:
        """Extract 3-5 main factual claims from the article."""
        prompt = f"""You are an expert fact-checker and critical thinking analyst. Your task is to identify the core factual claims in a news article.

ARTICLE TITLE: {article_data.get('title', 'Unknown')}
ARTICLE CONTENT: {article_data.get('content', '')[:3000]}

Instructions:
1. Identify 3-5 of the most important FACTUAL CLAIMS (not opinions) made in this article
2. Focus on claims that are:
   - Specific and verifiable
   - Central to the article's main narrative
   - Presented as facts rather than speculation
3. Present each claim as a clear, concise bullet point
4. Avoid including obvious background information or widely accepted facts

Format your response as a simple list of claims, one per line, starting with "• "

Example format:
• Company X reported a 25% increase in quarterly revenue
• The new policy will affect over 100,000 residents
• Three independent studies confirmed the correlation

Your analysis:"""

        response = self._get_ai_response(prompt)
        return self._parse_bullet_points(response)

    def _analyze_language_and_tone(self, article_data: Dict[str, str]) -> str:
        """Analyze the language and tone of the article."""
        prompt = f"""You are a linguistics expert specializing in media analysis and bias detection. Analyze the language and tone of this news article.

ARTICLE TITLE: {article_data.get('title', 'Unknown')}
ARTICLE CONTENT: {article_data.get('content', '')[:3000]}

Provide a detailed analysis (2-3 sentences) that addresses:

1. TONE CLASSIFICATION: Is the tone neutral/objective, persuasive/advocacy, sensationalist, academic, or opinion-based?

2. LANGUAGE PATTERNS: Note specific linguistic choices such as:
   - Emotional or charged language vs. neutral terminology
   - Active vs. passive voice usage
   - Certainty vs. hedging language ("definitely" vs. "appears to")
   - Use of superlatives or absolute statements

3. RHETORICAL TECHNIQUES: Identify any persuasive techniques like:
   - Appeal to emotion, authority, or fear
   - Use of loaded questions or leading statements
   - Selective emphasis or framing

4. OBJECTIVITY ASSESSMENT: Rate how the language suggests the author's stance

Write a cohesive paragraph that synthesizes these observations into an overall assessment of the article's linguistic approach."""

        return self._get_ai_response(prompt).strip()

    def _identify_red_flags(self, article_data: Dict[str, str]) -> List[str]:
        """Identify potential signs of bias or poor reporting."""
        prompt = f"""You are an experienced journalism ethics expert and media literacy educator. Analyze this article for potential red flags that indicate bias, poor reporting, or misleading information.

ARTICLE TITLE: {article_data.get('title', 'Unknown')}
ARTICLE CONTENT: {article_data.get('content', '')[:3000]}

Look for these specific red flags and ONLY list ones you can actually identify in the text:

SOURCE ISSUES:
- Over-reliance on anonymous sources for major claims
- Lack of diverse perspectives or one-sided sourcing
- Missing attribution for important statistics or claims
- Conflicts of interest not disclosed

LOGICAL/METHODOLOGICAL ISSUES:
- Correlation presented as causation
- Anecdotal evidence treated as representative
- Missing context or cherry-picked data
- Unsupported generalizations

LANGUAGE/PRESENTATION ISSUES:
- Loaded or emotionally manipulative language
- False dichotomies or oversimplification
- Sensationalized headlines vs. content mismatch
- Opinion presented as fact

TRANSPARENCY ISSUES:
- Vague timeframes or locations
- Missing links to source documents/studies
- Unclear methodology for surveys or studies mentioned

Format as bullet points starting with "• " and be specific about what you observed.
If you cannot identify clear red flags, state "No significant red flags detected in the available content."""

        response = self._get_ai_response(prompt)
        if "no significant red flags detected" in response.lower():
            return ["No significant red flags detected in the available content."]
        return self._parse_bullet_points(response)

    def _generate_verification_questions(self, article_data: Dict[str, str]) -> List[str]:
        """Generate specific, actionable verification questions."""
        prompt = f"""You are a professional fact-checker and investigative journalist. Create specific, actionable questions that readers should ask to independently verify this article's content.

ARTICLE TITLE: {article_data.get('title', 'Unknown')}
ARTICLE CONTENT: {article_data.get('content', '')[:3000]}
AUTHOR(S): {article_data.get('authors', 'Unknown')}

Create 3-4 sharp, specific verification questions that are:

1. ACTIONABLE: Questions readers can actually investigate
2. TARGETED: Focus on the most important or questionable claims
3. SPECIFIC: Not generic questions that apply to any article
4. STRATEGIC: Address potential weak points in the reporting

Good examples:
- "What is the methodology and sample size of the survey mentioned, and who funded it?"
- "Can the economic data cited be verified through official government statistics?"
- "Do other credible news sources corroborate the anonymous insider's claims?"

Avoid generic questions like:
- "Is this source reliable?" 
- "What do experts think?"

Format as numbered questions (1., 2., 3., 4.)"""

        response = self._get_ai_response(prompt)
        return self._parse_numbered_list(response)

    def _perform_entity_recognition(self, article_data: Dict[str, str]) -> Dict[str, List[str]]:
        """Identify key entities and suggest investigation points."""
        prompt = f"""You are an investigative researcher. Identify the key entities (people, organizations, locations) mentioned in this article and suggest what readers should investigate about them.

ARTICLE CONTENT: {article_data.get('content', '')[:2000]}

For each significant entity mentioned, provide investigation suggestions. Focus on entities that are:
- Central to the main claims
- Sources of information or quotes
- Organizations funding studies or research
- Government agencies or officials mentioned

Format as:
PEOPLE:
• Name - Investigation suggestion

ORGANIZATIONS:
• Name - Investigation suggestion  

LOCATIONS (if relevant):
• Location - Investigation suggestion

Be selective - only include entities worth investigating, not every person/place mentioned."""

        response = self._get_ai_response(prompt)
        return self._parse_entity_response(response)

    def _generate_counter_argument(self, article_data: Dict[str, str]) -> str:
        """Generate a counter-argument to highlight potential biases."""
        prompt = f"""You are playing devil's advocate. Read this article and then briefly summarize how someone with an opposing viewpoint might interpret or challenge the same information.

ARTICLE TITLE: {article_data.get('title', 'Unknown')}
ARTICLE CONTENT: {article_data.get('content', '')[:2500]}

Consider:
1. What alternative explanations might exist for the events described?
2. What context or information might be missing that could change the narrative?
3. What assumptions does the article make that could be questioned?
4. How might stakeholders with different interests interpret these same facts?

Write a brief paragraph (3-4 sentences) presenting this alternative perspective. Be fair and thoughtful - this isn't about being contrarian, but about highlighting how the same information can be interpreted differently.

Start with: "An opposing perspective might argue that..."""

        return self._get_ai_response(prompt).strip()

    def _get_ai_response(self, prompt: str) -> str:
        """Get response from OpenAI API with error handling and retries."""
        for attempt in range(Config.MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model=Config.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are an expert in critical thinking, journalism ethics, and media analysis. Provide precise, insightful analysis that helps users think critically about information."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.3  # Lower temperature for more consistent, analytical responses
                )
                return response.choices[0].message.content.strip()

            except Exception as e:
                if attempt == Config.MAX_RETRIES - 1:
                    raise AIAnalysisError(f"Failed to get AI response after {Config.MAX_RETRIES} attempts: {str(e)}")
                continue

    def _parse_bullet_points(self, text: str) -> List[str]:
        """Parse bullet points from AI response."""
        lines = text.split('\n')
        bullet_points = []

        for line in lines:
            line = line.strip()
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                bullet_points.append(line[1:].strip())

        return bullet_points if bullet_points else [text.strip()]

    def _parse_numbered_list(self, text: str) -> List[str]:
        """Parse numbered list from AI response."""
        lines = text.split('\n')
        numbered_items = []

        for line in lines:
            line = line.strip()
            if re.match(r'^\d+\.', line):
                numbered_items.append(re.sub(r'^\d+\.\s*', '', line))

        return numbered_items if numbered_items else [text.strip()]

    def _parse_entity_response(self, text: str) -> Dict[str, List[str]]:
        """Parse entity recognition response."""
        entities = {'people': [], 'organizations': [], 'locations': []}
        current_category = None

        lines = text.split('\n')
        for line in lines:
            line = line.strip()

            if 'PEOPLE:' in line.upper():
                current_category = 'people'
            elif 'ORGANIZATIONS:' in line.upper():
                current_category = 'organizations'
            elif 'LOCATIONS:' in line.upper():
                current_category = 'locations'
            elif line.startswith('•') and current_category:
                entities[current_category].append(line[1:].strip())

        return entities
