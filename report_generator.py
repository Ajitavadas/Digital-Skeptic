from typing import Dict, List
from datetime import datetime


class ReportGenerator:
    """Generates professional Markdown reports from analysis results."""

    def generate_report(self, analysis_results: Dict[str, any]) -> str:
        """
        Generate a comprehensive Critical Analysis Report in Markdown format.

        Args:
            analysis_results (Dict[str, any]): Results from DigitalSkepticAnalyzer

        Returns:
            str: Formatted Markdown report
        """
        metadata = analysis_results.get('article_metadata', {})
        title = metadata.get('title', 'Unknown Article')

        # Build the report sections
        report_sections = [
            self._generate_header(metadata),
            self._generate_core_claims(analysis_results.get('core_claims', [])),
            self._generate_language_analysis(analysis_results.get('language_analysis', '')),
            self._generate_red_flags(analysis_results.get('red_flags', [])),
            self._generate_verification_questions(analysis_results.get('verification_questions', [])),
            self._generate_entity_investigation(analysis_results.get('entities', {})),
            self._generate_counter_argument(analysis_results.get('counter_argument', '')),
            self._generate_footer()
        ]

        return '\n\n'.join(filter(None, report_sections))

    def _generate_header(self, metadata: Dict[str, str]) -> str:
        """Generate report header with article metadata."""
        title = metadata.get('title', 'Unknown Article')
        url = metadata.get('url', '')
        authors = metadata.get('authors', 'Unknown Author')
        publish_date = metadata.get('publish_date', 'Unknown Date')

        header = f"# Critical Analysis Report: {title}\n"

        if url:
            header += f"**Source URL:** {url}\n"
        if authors != 'Unknown Author':
            header += f"**Author(s):** {authors}\n"
        if publish_date != 'Unknown Date':
            header += f"**Published:** {publish_date}\n"

        header += f"**Analysis Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n"
        header += "---\n"
        header += "*This report provides a critical analysis to help readers evaluate the article's claims, sources, and potential biases. It does not determine truth or falsehood, but rather highlights areas that warrant further investigation.*"

        return header

    def _generate_core_claims(self, claims: List[str]) -> str:
        """Generate Core Claims section."""
        if not claims:
            return "### Core Claims\n\n*No specific factual claims could be identified in the available content.*"

        section = "### Core Claims\n\n"
        section += "*The following are the main factual assertions made in this article:*\n\n"

        for claim in claims:
            section += f"• {claim}\n"

        return section

    def _generate_language_analysis(self, analysis: str) -> str:
        """Generate Language & Tone Analysis section."""
        if not analysis:
            return "### Language & Tone Analysis\n\n*Unable to perform language analysis on the available content.*"

        section = "### Language & Tone Analysis\n\n"
        section += analysis

        return section

    def _generate_red_flags(self, red_flags: List[str]) -> str:
        """Generate Potential Red Flags section."""
        section = "### Potential Red Flags\n\n"

        if not red_flags or (len(red_flags) == 1 and "no significant red flags detected" in red_flags[0].lower()):
            section += "*No significant red flags detected in the available content. However, readers should still verify information through independent sources.*"
            return section

        section += "*The following potential issues were identified that may indicate bias or require additional verification:*\n\n"

        for flag in red_flags:
            section += f"• {flag}\n"

        return section

    def _generate_verification_questions(self, questions: List[str]) -> str:
        """Generate Verification Questions section."""
        if not questions:
            return "### Verification Questions\n\n*Unable to generate specific verification questions for this content.*"

        section = "### Verification Questions\n\n"
        section += "*Consider investigating these specific questions to verify the article's content:*\n\n"

        for i, question in enumerate(questions, 1):
            section += f"{i}. {question}\n"

        return section

    def _generate_entity_investigation(self, entities: Dict[str, List[str]]) -> str:
        """Generate Entity Investigation Guide (stand-out feature)."""
        if not any(entities.values()):
            return ""

        section = "### Entity Investigation Guide\n\n"
        section += "*Key entities mentioned in the article and suggested investigation points:*\n\n"

        for category, entity_list in entities.items():
            if entity_list:
                section += f"**{category.upper()}:**\n"
                for entity in entity_list:
                    section += f"• {entity}\n"
                section += "\n"

        return section.rstrip()

    def _generate_counter_argument(self, counter_argument: str) -> str:
        """Generate Counter-Perspective section (stand-out feature)."""
        if not counter_argument:
            return ""

        section = "### Alternative Perspective\n\n"
        section += "*To highlight potential biases, consider this opposing viewpoint:*\n\n"
        section += f"> {counter_argument}"

        return section

    def _generate_footer(self) -> str:
        """Generate report footer with usage instructions."""
        footer = "---\n\n"
        footer += "### How to Use This Analysis\n\n"
        footer += "This critical analysis is designed to enhance your media literacy, not replace your judgment. Use it to:\n\n"
        footer += "• **Question assumptions** - Look beyond surface-level claims\n"
        footer += "• **Seek additional sources** - Cross-reference with other reputable outlets\n"
        footer += "• **Investigate entities** - Research the background of people and organizations mentioned\n"
        footer += "• **Consider context** - Look for information that might be missing\n"
        footer += "• **Think critically** - Form your own conclusions based on evidence\n\n"
        footer += "*Remember: The goal is not to dismiss information, but to evaluate it more thoughtfully.*"

        return footer


class ConsoleReporter:
    """Handles console output and progress reporting."""

    @staticmethod
    def print_progress(message: str):
        """Print progress message to console."""
        print(f"[DIGITAL SKEPTIC] {message}")

    @staticmethod
    def print_error(error_message: str):
        """Print error message to console."""
        print(f"[ERROR] {error_message}")

    @staticmethod
    def print_success(message: str):
        """Print success message to console."""
        print(f"[SUCCESS] {message}")

    @staticmethod
    def print_article_info(article_data: Dict[str, str]):
        """Print extracted article information."""
        print("\n" + "="*60)
        print("ARTICLE INFORMATION")
        print("="*60)
        print(f"Title: {article_data.get('title', 'Unknown')}")
        print(f"Author(s): {article_data.get('authors', 'Unknown')}")
        print(f"URL: {article_data.get('url', 'Unknown')}")
        print(f"Content Length: {len(article_data.get('content', ''))} characters")
        print(f"Extraction Method: {article_data.get('extraction_method', 'Unknown')}")
        print("="*60 + "\n")
