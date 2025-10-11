#!/usr/bin/env python3
"""
Comprehensive Multilingual Analysis - Generate 5 Reports
Creates Q4, Q8, F16, Comparison, and Overall multilingual reports
"""

import csv
from collections import defaultdict
from typing import Dict, List

LANGUAGES = {
    'en': 'English',
    'fr': 'French',
    'de': 'German',
    'es': 'Spanish',
    'ar': 'Arabic',
    'zh': 'Chinese'
}

def load_and_parse_csv(filepath: str = 'test_results_multilang.csv') -> Dict[str, List[Dict]]:
    """Load CSV and group by quantization type."""
    results = {
        'Q4_K_M': [],
        'Q8_0': [],
        'F16': [],
        'ALL': []
    }

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse fields
            row['response_time_seconds'] = float(row['response_time_seconds']) if row['response_time_seconds'] else 0
            row['model_size_mb'] = float(row['model_size_mb'])
            row['correct_answer'] = row['correct_answer'] == 'TRUE'
            row['success'] = row['success'] == 'TRUE'

            # Determine quantization
            model_name = row['model_name']
            if 'Q4_K_M' in model_name:
                quant_type = 'Q4_K_M'
            elif 'Q8_0' in model_name:
                quant_type = 'Q8_0'
            elif 'F16' in model_name:
                quant_type = 'F16'
            else:
                continue

            results[quant_type].append(row)
            results['ALL'].append(row)

    return results

def calculate_model_stats(data: List[Dict]) -> Dict:
    """Calculate statistics per model."""
    model_stats = defaultdict(lambda: {
        'total': 0,
        'correct': 0,
        'times': [],
        'size_mb': 0,
        'languages': defaultdict(lambda: {'total': 0, 'correct': 0, 'times': []}),
        'domains': defaultdict(lambda: {'total': 0, 'correct': 0})
    })

    for row in data:
        if not row['success']:
            continue

        # Remove quantization suffix for grouping
        model = row['model_name'].rsplit('-', 1)[0] if any(q in row['model_name'] for q in ['Q4_K_M', 'Q8_0', 'F16']) else row['model_name']
        stats = model_stats[model]

        stats['total'] += 1
        stats['size_mb'] = row['model_size_mb']
        stats['times'].append(row['response_time_seconds'])

        if row['correct_answer']:
            stats['correct'] += 1

        # Language-specific
        lang = row['language']
        stats['languages'][lang]['total'] += 1
        stats['languages'][lang]['times'].append(row['response_time_seconds'])
        if row['correct_answer']:
            stats['languages'][lang]['correct'] += 1

        # Domain-specific
        domain = row['domain']
        stats['domains'][domain]['total'] += 1
        if row['correct_answer']:
            stats['domains'][domain]['correct'] += 1

    # Calculate averages
    for model, stats in model_stats.items():
        stats['accuracy'] = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        stats['avg_time'] = sum(stats['times']) / len(stats['times']) if stats['times'] else 0

        for lang in stats['languages'].values():
            lang['accuracy'] = (lang['correct'] / lang['total'] * 100) if lang['total'] > 0 else 0
            lang['avg_time'] = sum(lang['times']) / len(lang['times']) if lang['times'] else 0

    return dict(model_stats)

def format_time(seconds: float) -> str:
    return f"{int(seconds * 1000)}ms"

def format_size(mb: float) -> str:
    if mb >= 1000:
        return f"{mb/1000:.1f} GB"
    return f"{int(mb)} MB"

def generate_quant_report(quant_type: str, stats: Dict, total_tests: int) -> str:
    """Generate report for a single quantization."""

    if not stats:
        return f"# Multilingual Report - {quant_type}\n\nNo data available for this quantization.\n"

    report = f"""# Multilingual Reranking Benchmark - {quant_type} Quantization

## Executive Summary

**Quantization:** {quant_type}
**Tests Completed:** {total_tests}
**Models Tested:** {len(stats)}
**Languages:** 6 (English, French, German, Spanish, Arabic, Chinese)
**Domains per Language:** 10

"""

    # Overall stats
    avg_accuracy = sum(s['accuracy'] for s in stats.values()) / len(stats)
    avg_time = sum(s['avg_time'] for s in stats.values()) / len(stats)
    total_storage = sum(s['size_mb'] for s in stats.values())

    report += f"**Overall Accuracy:** {avg_accuracy:.1f}%\n"
    report += f"**Average Response Time:** {format_time(avg_time)}\n"
    report += f"**Total Storage:** {format_size(total_storage)}\n\n"

    # Perfect accuracy models
    perfect_models = [(m, s) for m, s in stats.items() if s['accuracy'] == 100]
    report += f"**Perfect Accuracy Models (100%):** {len(perfect_models)}\n\n"

    # Top 10 overall
    report += "## Top 10 Models - Overall Performance\n\n"
    sorted_models = sorted(stats.items(), key=lambda x: (-x[1]['accuracy'], x[1]['avg_time']))[:10]

    report += "| Rank | Model | Accuracy | Avg Time | Size | Queries |\n"
    report += "|------|-------|----------|----------|------|----------|\n"

    for i, (model, s) in enumerate(sorted_models, 1):
        emoji = "🏆" if i == 1 else "⭐" if i <= 3 else ""
        report += f"| {i} {emoji} | {model} | {s['accuracy']:.1f}% | {format_time(s['avg_time'])} | {format_size(s['size_mb'])} | {s['correct']}/{s['total']} |\n"

    # Language-specific performance
    report += "\n## Performance by Language\n\n"

    for lang_code, lang_name in sorted(LANGUAGES.items()):
        lang_stats = {}
        for model, s in stats.items():
            if lang_code in s['languages']:
                lang_stats[model] = s['languages'][lang_code]

        if not lang_stats:
            continue

        avg_lang_acc = sum(ls['accuracy'] for ls in lang_stats.values()) / len(lang_stats)
        perfect_lang = sum(1 for ls in lang_stats.values() if ls['accuracy'] == 100)

        report += f"### {lang_name} ({lang_code})\n"
        report += f"- Average Accuracy: {avg_lang_acc:.1f}%\n"
        report += f"- Models with 100%: {perfect_lang}\n"

        # Top 5 for this language
        top_lang = sorted(lang_stats.items(), key=lambda x: (-x[1]['accuracy'], x[1]['avg_time']))[:5]
        report += f"- **Top 5:** "
        report += ", ".join([f"{m} ({ls['accuracy']:.0f}%)" for m, ls in top_lang])
        report += "\n\n"

    # Multilingual consistency
    report += "## Multilingual Consistency\n\n"
    report += "Models performing well across ALL languages:\n\n"

    consistent_models = {}
    for model, s in stats.items():
        if len(s['languages']) == len(LANGUAGES):
            min_acc = min(lang['accuracy'] for lang in s['languages'].values())
            max_acc = max(lang['accuracy'] for lang in s['languages'].values())
            consistent_models[model] = {
                'min': min_acc,
                'max': max_acc,
                'avg': s['accuracy'],
                'variance': max_acc - min_acc
            }

    sorted_consistent = sorted(consistent_models.items(), key=lambda x: (-x[1]['min'], -x[1]['avg']))[:10]

    report += "| Rank | Model | Min | Max | Avg | Variance |\n"
    report += "|------|-------|-----|-----|-----|----------|\n"

    for i, (model, c) in enumerate(sorted_consistent, 1):
        emoji = "🌍" if i == 1 else ""
        report += f"| {i} {emoji} | {model} | {c['min']:.1f}% | {c['max']:.1f}% | {c['avg']:.1f}% | {c['variance']:.1f}% |\n"

    # Language matrix
    report += "\n## Language Performance Matrix (Top 10)\n\n"
    report += "| Model | " + " | ".join(LANGUAGES.values()) + " |\n"
    report += "|-------|" + "|".join(["-----"] * len(LANGUAGES)) + "|\n"

    for model, s in sorted_models[:10]:
        row = f"| {model} |"
        for lang_code in sorted(LANGUAGES.keys()):
            if lang_code in s['languages']:
                row += f" {s['languages'][lang_code]['accuracy']:.0f}% |"
            else:
                row += " - |"
        report += row + "\n"

    # Key findings
    report += "\n## Key Findings\n\n"

    if stats:
        fastest = min(stats.items(), key=lambda x: x[1]['avg_time'])
        slowest = max(stats.items(), key=lambda x: x[1]['avg_time'])
        report += f"- **Speed Range:** {format_time(fastest[1]['avg_time'])} ({fastest[0]}) to {format_time(slowest[1]['avg_time'])} ({slowest[0]})\n"

        smallest = min(stats.items(), key=lambda x: x[1]['size_mb'])
        largest = max(stats.items(), key=lambda x: x[1]['size_mb'])
        report += f"- **Size Range:** {format_size(smallest[1]['size_mb'])} ({smallest[0]}) to {format_size(largest[1]['size_mb'])} ({largest[0]})\n"

        very_consistent = [m for m, c in consistent_models.items() if c['variance'] < 10]
        if very_consistent:
            report += f"- **Language-Agnostic Models** (variance <10%): {len(very_consistent)} models\n"

        if perfect_models:
            report += f"- **Perfect Score Models:** {', '.join([m for m, _ in perfect_models[:5]])}\n"

    return report

def generate_comparison_report(all_stats: Dict) -> str:
    """Generate cross-quantization comparison report."""

    report = """# Multilingual Performance - Quantization Comparison

## Overview

This report compares multilingual performance across three quantization levels.

## Quantization Summary

"""

    # Summary table
    report += "| Quantization | Models | Avg Accuracy | Avg Time | Perfect 100% |\n"
    report += "|--------------|--------|--------------|----------|---------------|\n"

    quant_summary = {}
    for quant in ['F16', 'Q8_0', 'Q4_K_M']:
        stats = all_stats.get(quant, {})
        if stats:
            avg_acc = sum(s['accuracy'] for s in stats.values()) / len(stats)
            avg_time = sum(s['avg_time'] for s in stats.values()) / len(stats)
            perfect = sum(1 for s in stats.values() if s['accuracy'] == 100)
            quant_summary[quant] = {'acc': avg_acc, 'time': avg_time, 'perfect': perfect, 'count': len(stats)}
            report += f"| {quant} | {len(stats)} | {avg_acc:.1f}% | {format_time(avg_time)} | {perfect} |\n"

    # Model family comparison
    report += "\n## Model Family Comparison\n\n"

    # Find models in all quantizations
    model_families = defaultdict(dict)
    for quant, stats in all_stats.items():
        if quant == 'ALL':
            continue
        for model, s in stats.items():
            model_families[model][quant] = s

    complete_models = {m: data for m, data in model_families.items() if len(data) == 3}

    if complete_models:
        report += f"### Top Models Available in All Quantizations ({len(complete_models)} models)\n\n"

        # Sort by F16 accuracy
        sorted_families = sorted(complete_models.items(), key=lambda x: -x[1].get('F16', {}).get('accuracy', 0))[:10]

        for model, quant_data in sorted_families:
            report += f"**{model}**\n\n"
            report += "| Quant | Accuracy | Time | Size | Languages Tested |\n"
            report += "|-------|----------|------|------|------------------|\n"

            for quant in ['F16', 'Q8_0', 'Q4_K_M']:
                if quant in quant_data:
                    s = quant_data[quant]
                    report += f"| {quant} | {s['accuracy']:.1f}% | {format_time(s['avg_time'])} | {format_size(s['size_mb'])} | {len(s['languages'])} |\n"

            report += "\n"

    # Language-specific quantization impact
    report += "\n## Quantization Impact by Language\n\n"

    for lang_code, lang_name in sorted(LANGUAGES.items()):
        report += f"### {lang_name}\n\n"
        report += "| Quantization | Avg Accuracy | Best Model | Best Accuracy |\n"
        report += "|--------------|--------------|------------|---------------|\n"

        for quant in ['F16', 'Q8_0', 'Q4_K_M']:
            stats = all_stats.get(quant, {})
            if stats:
                lang_accs = []
                best_model = None
                best_acc = 0

                for model, s in stats.items():
                    if lang_code in s['languages']:
                        acc = s['languages'][lang_code]['accuracy']
                        lang_accs.append(acc)
                        if acc > best_acc:
                            best_acc = acc
                            best_model = model

                if lang_accs:
                    avg_acc = sum(lang_accs) / len(lang_accs)
                    report += f"| {quant} | {avg_acc:.1f}% | {best_model or 'N/A'} | {best_acc:.0f}% |\n"

        report += "\n"

    # Recommendations
    report += "\n## Recommendations\n\n"

    report += "### By Use Case:\n\n"
    report += "**Production Deployment (Balanced):**\n"
    q4_stats = all_stats.get('Q4_K_M', {})
    if q4_stats:
        top_q4 = sorted(q4_stats.items(), key=lambda x: (-x[1]['accuracy'], x[1]['avg_time']))[:3]
        for i, (model, s) in enumerate(top_q4, 1):
            report += f"{i}. {model} - {s['accuracy']:.0f}%, {format_time(s['avg_time'])}, {format_size(s['size_mb'])}\n"

    report += "\n**Maximum Quality:**\n"
    f16_stats = all_stats.get('F16', {})
    if f16_stats:
        top_f16 = sorted(f16_stats.items(), key=lambda x: (-x[1]['accuracy'], x[1]['avg_time']))[:3]
        for i, (model, s) in enumerate(top_f16, 1):
            report += f"{i}. {model} - {s['accuracy']:.0f}%, {format_time(s['avg_time'])}, {format_size(s['size_mb'])}\n"

    report += "\n**Balance (Q8):**\n"
    q8_stats = all_stats.get('Q8_0', {})
    if q8_stats:
        top_q8 = sorted(q8_stats.items(), key=lambda x: (-x[1]['accuracy'], x[1]['avg_time']))[:3]
        for i, (model, s) in enumerate(top_q8, 1):
            report += f"{i}. {model} - {s['accuracy']:.0f}%, {format_time(s['avg_time'])}, {format_size(s['size_mb'])}\n"

    return report

def generate_overall_report(stats: Dict, total_tests: int) -> str:
    """Generate overall cross-quantization report."""

    report = """# Multilingual Reranking - Overall Analysis

## Executive Summary

This report aggregates performance across ALL quantizations and languages.

"""

    if not stats:
        return report + "No data available.\n"

    avg_accuracy = sum(s['accuracy'] for s in stats.values()) / len(stats)
    avg_time = sum(s['avg_time'] for s in stats.values()) / len(stats)

    report += f"**Total Tests:** {total_tests}\n"
    report += f"**Unique Models:** {len(stats)}\n"
    report += f"**Overall Accuracy:** {avg_accuracy:.1f}%\n"
    report += f"**Average Time:** {format_time(avg_time)}\n\n"

    # Top 15 models overall
    report += "## Top 15 Models - Aggregated Performance\n\n"
    sorted_models = sorted(stats.items(), key=lambda x: (-x[1]['accuracy'], x[1]['avg_time']))[:15]

    report += "| Rank | Model | Accuracy | Time | Size | Tests |\n"
    report += "|------|-------|----------|------|------|-------|\n"

    for i, (model, s) in enumerate(sorted_models, 1):
        emoji = "🏆" if i == 1 else "⭐" if i <= 3 else ""
        report += f"| {i} {emoji} | {model} | {s['accuracy']:.1f}% | {format_time(s['avg_time'])} | {format_size(s['size_mb'])} | {s['total']} |\n"

    # Best per language (aggregated)
    report += "\n## Best Model per Language (Aggregated)\n\n"

    for lang_code, lang_name in sorted(LANGUAGES.items()):
        best_model = None
        best_acc = 0

        for model, s in stats.items():
            if lang_code in s['languages']:
                acc = s['languages'][lang_code]['accuracy']
                if acc > best_acc:
                    best_acc = acc
                    best_model = model

        if best_model:
            report += f"**{lang_name}:** {best_model} ({best_acc:.0f}%)\n"

    return report

def main():
    """Main analysis function."""
    print("Loading multilingual test results...")
    data = load_and_parse_csv()

    print(f"Processing data:")
    print(f"  F16: {len(data['F16'])} tests")
    print(f"  Q8_0: {len(data['Q8_0'])} tests")
    print(f"  Q4_K_M: {len(data['Q4_K_M'])} tests")
    print(f"  ALL: {len(data['ALL'])} tests")

    print("\nCalculating statistics...")
    all_stats = {}
    for quant in ['Q4_K_M', 'Q8_0', 'F16', 'ALL']:
        all_stats[quant] = calculate_model_stats(data[quant])
        print(f"  {quant}: {len(all_stats[quant])} models")

    print("\nGenerating reports...")

    # Individual quantization reports
    for quant in ['Q4_K_M', 'Q8_0', 'F16']:
        report = generate_quant_report(quant, all_stats[quant], len(data[quant]))
        filename = f"REPORT_MULTILANG_{quant}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"  ✓ {filename}")

    # Comparison report
    comparison = generate_comparison_report(all_stats)
    with open('REPORT_MULTILANG_COMPARISON.md', 'w', encoding='utf-8') as f:
        f.write(comparison)
    print(f"  ✓ REPORT_MULTILANG_COMPARISON.md")

    # Overall report
    overall = generate_overall_report(all_stats['ALL'], len(data['ALL']))
    with open('REPORT_MULTILANG_OVERALL.md', 'w', encoding='utf-8') as f:
        f.write(overall)
    print(f"  ✓ REPORT_MULTILANG_OVERALL.md")

    print("\n✅ All 5 multilingual reports generated!")
    print("\nReport files:")
    print("  - REPORT_MULTILANG_Q4_K_M.md")
    print("  - REPORT_MULTILANG_Q8_0.md")
    print("  - REPORT_MULTILANG_F16.md")
    print("  - REPORT_MULTILANG_COMPARISON.md")
    print("  - REPORT_MULTILANG_OVERALL.md")

if __name__ == '__main__':
    main()
