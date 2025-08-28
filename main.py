#!/usr/bin/env python3
"""
Digital Skeptic AI - Critical Analysis Tool for News Articles
Hackathon Mission 2: Empowering Critical Thinking in an Age of Information Overload

This tool analyzes news articles for bias, claims, and provides verification questions
to help users think critically about information they consume.
"""

import sys
import argparse
from pathlib import Path

from article_scraper import ArticleScraper, ArticleScrapingError
from ai_analyzer import DigitalSkepticAnalyzer, AIAnalysisError
from report_generator import ReportGenerator, ConsoleReporter
from config import Config


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Digital Skeptic AI - Critical Analysis Tool for News Articles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py https://example.com/news-article
  python main.py https://example.com/news-article --output report.md
  python main.py https://example.com/news-article --debug
        """
    )

    parser.add_argument(
        'url',
        help='URL of the news article to analyze'
    )

    parser.add_argument(
        '--output', '-o',
        default='critical_analysis_report.md',
        help='Output file path for the analysis report (default: critical_analysis_report.md)'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode for detailed error messages'
    )

    args = parser.parse_args()

    # Set debug mode if requested
    if args.debug:
        Config.DEBUG_MODE = True

    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        ConsoleReporter.print_error(str(e))
        ConsoleReporter.print_error("Please check your .env file or environment variables.")
        sys.exit(1)

    try:
        # Initialize components
        ConsoleReporter.print_progress("Initializing Digital Skeptic AI...")

        scraper = ArticleScraper()
        analyzer = DigitalSkepticAnalyzer()
        generator = ReportGenerator()

        # Extract article content
        ConsoleReporter.print_progress(f"Extracting content from: {args.url}")
        article_data = scraper.extract_article(args.url)

        # Display article information
        ConsoleReporter.print_article_info(article_data)

        # Perform AI analysis
        ConsoleReporter.print_progress("Performing critical analysis...")
        analysis_results = analyzer.analyze_article(article_data)

        # Generate report
        ConsoleReporter.print_progress("Generating analysis report...")
        report = generator.generate_report(analysis_results)

        # Save report to file
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        # Success message
        ConsoleReporter.print_success(f"Critical analysis report saved to: {output_path.absolute()}")

        # Display preview of report
        print("\n" + "="*60)
        print("REPORT PREVIEW")
        print("="*60)
        print(report[:500] + "..." if len(report) > 500 else report)
        print("="*60)

        return 0

    except ArticleScrapingError as e:
        ConsoleReporter.print_error(f"Failed to extract article content: {str(e)}")
        if Config.DEBUG_MODE:
            import traceback
            traceback.print_exc()
        return 1

    except AIAnalysisError as e:
        ConsoleReporter.print_error(f"AI analysis failed: {str(e)}")
        if Config.DEBUG_MODE:
            import traceback
            traceback.print_exc()
        return 1

    except Exception as e:
        ConsoleReporter.print_error(f"Unexpected error: {str(e)}")
        if Config.DEBUG_MODE:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
