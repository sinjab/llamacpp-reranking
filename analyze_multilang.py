#!/usr/bin/env python3
"""
Multilingual Reranking Results Analysis
Generates comprehensive reports for multilingual model performance
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

def load_results(filepath: str = 'test_results_multilang.csv') -> List[Dict]:
    """Load multilingual test results from CSV."""
    results = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['response_time_seconds'] = float(row['response_time_seconds']) if row['response_time_seconds'] else 0
            row['model_size_mb'] = float(row['model_size_mb'])
            row['correct_answer'] = row['correct_answer'] == 'True'
            row['success'] = row['success'] == 'True'
            results.append(row)
    return results

def calculate_model_stats(data: List[Dict]) -> Dict:
    """Calculate statistics per model across all languages."""
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

        model = row['model_name']
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

def format_size(mb: float) -> str:
    """Format size in MB or GB."""
    if mb >= 1000:
        return f"{mb/1000:.1f} GB"
    return f"{int(mb)} MB"

def generate_report(stats: Dict, total_tests: int) -> str:
    """Generate comprehensive multilingual analysis report."""

    report = """# Multilingual Reranking Models Benchmark Report

## Executive Summary

"""

    # Overall stats
    total_models = len(stats)
    avg_accuracy = sum(s['accuracy'] for s in stats.values()) / len(stats) if stats else 0
    avg_time = sum(s['avg_time'] for s in stats.values()) / len(stats) if stats else 0

    report += f"**Tests Completed:** {total_tests}\n"
    report += f"**Models Tested:** {total_models}\n"
    report += f"**Languages:** 6 ({', '.join(LANGUAGES.values())})\n"
    report += f"**Overall Accuracy:** {avg_accuracy:.1f}%\n"
    report += f"**Average Response Time:** {int(avg_time * 1000)}ms\n\n"

    # Top performers overall
    report += "## Top 10 Models - Overall Performance\n\n"

    sorted_models = sorted(stats.items(), key=lambda x: (-x[1]['accuracy'], x[1]['avg_time']))[:10]

    report += "| Rank | Model | Accuracy | Avg Time | Size |\n"
    report += "|------|-------|----------|----------|------|\n"

    for i, (model, s) in enumerate(sorted_models, 1):
        emoji = "🏆" if i == 1 else "⭐" if i <= 3 else ""
        report += f"| {i} {emoji} | {model} | {s['accuracy']:.1f}% | {int(s['avg_time']*1000)}ms | {format_size(s['size_mb'])} |\n"

    # Perfect accuracy models
    perfect_models = [(m, s) for m, s in stats.items() if s['accuracy'] == 100]
    if perfect_models:
        report += f"\n### Perfect Accuracy Models (100%) - {len(perfect_models)} models\n\n"
        perfect_models.sort(key=lambda x: x[1]['avg_time'])

        for model, s in perfect_models:
            report += f"**{model}**\n"
            report += f"- Speed: {int(s['avg_time']*1000)}ms | Size: {format_size(s['size_mb'])}\n"
            report += f"- Tested: {s['total']} queries across {len(s['languages'])} languages\n\n"

    # Language-specific performance
    report += "\n## Performance by Language\n\n"

    for lang_code, lang_name in sorted(LANGUAGES.items()):
        report += f"### {lang_name} ({lang_code})\n\n"

        # Calculate language-specific stats
        lang_stats = {}
        for model, s in stats.items():
            if lang_code in s['languages']:
                lang_data = s['languages'][lang_code]
                lang_stats[model] = lang_data

        if not lang_stats:
            report += "No data available.\n\n"
            continue

        avg_lang_acc = sum(ls['accuracy'] for ls in lang_stats.values()) / len(lang_stats)
        perfect_lang = sum(1 for ls in lang_stats.values() if ls['accuracy'] == 100)

        report += f"**Language Statistics:**\n"
        report += f"- Average Accuracy: {avg_lang_acc:.1f}%\n"
        report += f"- Models with 100% accuracy: {perfect_lang}\n\n"

        # Top 5 models for this language
        top_lang_models = sorted(lang_stats.items(), key=lambda x: (-x[1]['accuracy'], x[1]['avg_time']))[:5]

        report += f"**Top 5 Models:**\n\n"
        for i, (model, ls) in enumerate(top_lang_models, 1):
            report += f"{i}. **{model}** - {ls['accuracy']:.1f}% ({ls['correct']}/{ls['total']}) - {int(ls['avg_time']*1000)}ms\n"

        report += "\n"

    # Multilingual consistency analysis
    report += "\n## Multilingual Consistency Analysis\n\n"
    report += "Models that perform consistently well across all languages:\n\n"

    # Find models tested on all languages
    consistent_models = {}
    for model, s in stats.items():
        if len(s['languages']) == len(LANGUAGES):
            min_acc = min(lang['accuracy'] for lang in s['languages'].values())
            max_acc = max(lang['accuracy'] for lang in s['languages'].values())
            std_dev = max_acc - min_acc
            consistent_models[model] = {
                'min': min_acc,
                'max': max_acc,
                'avg': s['accuracy'],
                'std_dev': std_dev,
                'size': s['size_mb'],
                'time': s['avg_time']
            }

    # Sort by minimum accuracy (most consistent)
    sorted_consistent = sorted(consistent_models.items(), key=lambda x: (-x[1]['min'], -x[1]['avg']))[:10]

    report += "| Rank | Model | Min Acc | Max Acc | Avg Acc | Variance | Size | Time |\n"
    report += "|------|-------|---------|---------|---------|----------|------|------|\n"

    for i, (model, c) in enumerate(sorted_consistent, 1):
        emoji = "🌍" if i == 1 else "🌎" if i <= 3 else ""
        report += f"| {i} {emoji} | {model} | {c['min']:.1f}% | {c['max']:.1f}% | {c['avg']:.1f}% | {c['std_dev']:.1f}% | {format_size(c['size'])} | {int(c['time']*1000)}ms |\n"

    # Language comparison heatmap
    report += "\n## Language Performance Matrix\n\n"
    report += "Top 10 models performance across all languages:\n\n"

    top_10_models = sorted(stats.items(), key=lambda x: (-x[1]['accuracy'], x[1]['avg_time']))[:10]

    report += "| Model | " + " | ".join(LANGUAGES.values()) + " | Overall |\n"
    report += "|-------|" + "|".join(["-----"] * len(LANGUAGES)) + "|--------|\n"

    for model, s in top_10_models:
        row = f"| {model} |"
        for lang_code in sorted(LANGUAGES.keys()):
            if lang_code in s['languages']:
                acc = s['languages'][lang_code]['accuracy']
                row += f" {acc:.0f}% |"
            else:
                row += " - |"
        row += f" {s['accuracy']:.0f}% |"
        report += row + "\n"

    # Domain analysis
    report += "\n## Domain Performance Analysis\n\n"

    # Aggregate domain performance across all models
    domain_agg = defaultdict(lambda: {'total': 0, 'correct': 0})
    for model, s in stats.items():
        for domain, d in s['domains'].items():
            domain_agg[domain]['total'] += d['total']
            domain_agg[domain]['correct'] += d['correct']

    report += "| Domain | Accuracy | Tests |\n"
    report += "|--------|----------|-------|\n"

    for domain in sorted(domain_agg.keys()):
        d = domain_agg[domain]
        acc = (d['correct'] / d['total'] * 100) if d['total'] > 0 else 0
        report += f"| {domain.capitalize()} | {acc:.1f}% | {d['total']} |\n"

    # Use case recommendations
    report += "\n## Use Case Recommendations\n\n"

    report += "### Best for Multilingual Applications\n"
    for i, (model, c) in enumerate(sorted_consistent[:3], 1):
        report += f"{i}. **{model}**\n"
        report += f"   - Consistent: {c['min']:.0f}%-{c['max']:.0f}% across all languages\n"
        report += f"   - Speed: {int(c['time']*1000)}ms | Size: {format_size(c['size'])}\n\n"

    report += "### Best for English-Only Applications\n"
    en_models = sorted(
        [(m, s['languages'].get('en', {})) for m, s in stats.items() if 'en' in s['languages']],
        key=lambda x: (-x[1].get('accuracy', 0), x[1].get('avg_time', 999))
    )[:3]
    for i, (model, en_data) in enumerate(en_models, 1):
        size = stats[model]['size_mb']
        report += f"{i}. **{model}** - {en_data['accuracy']:.0f}%, {int(en_data['avg_time']*1000)}ms, {format_size(size)}\n"

    report += "\n### Best for Asian Languages (Chinese, Arabic)\n"
    asian_models = []
    for model, s in stats.items():
        if 'zh' in s['languages'] and 'ar' in s['languages']:
            avg_asian = (s['languages']['zh']['accuracy'] + s['languages']['ar']['accuracy']) / 2
            asian_models.append((model, avg_asian, s['size_mb'], s['avg_time']))

    asian_models.sort(key=lambda x: (-x[1], x[3]))
    for i, (model, acc, size, time) in enumerate(asian_models[:3], 1):
        report += f"{i}. **{model}** - {acc:.0f}%, {int(time*1000)}ms, {format_size(size)}\n"

    report += "\n### Best for European Languages (French, German, Spanish)\n"
    euro_models = []
    for model, s in stats.items():
        if all(lang in s['languages'] for lang in ['fr', 'de', 'es']):
            avg_euro = sum(s['languages'][lang]['accuracy'] for lang in ['fr', 'de', 'es']) / 3
            euro_models.append((model, avg_euro, s['size_mb'], s['avg_time']))

    euro_models.sort(key=lambda x: (-x[1], x[3]))
    for i, (model, acc, size, time) in enumerate(euro_models[:3], 1):
        report += f"{i}. **{model}** - {acc:.0f}%, {int(time*1000)}ms, {format_size(size)}\n"

    # Key insights
    report += "\n## Key Insights\n\n"

    # Find models that are language-agnostic (similar performance across all)
    very_consistent = [(m, c) for m, c in consistent_models.items() if c['std_dev'] < 10]
    if very_consistent:
        report += f"- **{len(very_consistent)} models show language-agnostic behavior** (variance <10%): "
        report += ", ".join([m for m, _ in sorted(very_consistent, key=lambda x: -x[1]['min'])[:5]])
        report += "\n"

    # Find models that struggle with specific languages
    struggling = []
    for model, s in stats.items():
        if len(s['languages']) == len(LANGUAGES):
            for lang_code, lang_data in s['languages'].items():
                if lang_data['accuracy'] < 50 and s['accuracy'] > 70:
                    struggling.append((model, LANGUAGES[lang_code], lang_data['accuracy']))

    if struggling:
        report += f"- **Some models struggle with specific languages** despite good overall performance\n"

    # Speed comparison
    fastest = min(stats.items(), key=lambda x: x[1]['avg_time'])
    slowest = max(stats.items(), key=lambda x: x[1]['avg_time'])
    report += f"- **Speed range**: {int(fastest[1]['avg_time']*1000)}ms ({fastest[0]}) to {int(slowest[1]['avg_time']*1000)}ms ({slowest[0]})\n"

    # Size range
    smallest = min(stats.items(), key=lambda x: x[1]['size_mb'])
    largest = max(stats.items(), key=lambda x: x[1]['size_mb'])
    report += f"- **Size range**: {format_size(smallest[1]['size_mb'])} ({smallest[0]}) to {format_size(largest[1]['size_mb'])} ({largest[0]})\n"

    # Models with perfect score in specific language
    lang_perfect = defaultdict(list)
    for model, s in stats.items():
        for lang_code, lang_data in s['languages'].items():
            if lang_data['accuracy'] == 100:
                lang_perfect[lang_code].append(model)

    report += f"\n- **Models with 100% accuracy by language:**\n"
    for lang_code in sorted(LANGUAGES.keys()):
        lang_name = LANGUAGES[lang_code]
        count = len(lang_perfect[lang_code])
        report += f"  - {lang_name}: {count} models\n"

    return report

def main():
    """Main analysis function."""
    print("Loading multilingual test results...")
    data = load_results()

    print(f"Analyzing {len(data)} test results...")
    stats = calculate_model_stats(data)

    print(f"Generating report for {len(stats)} models...")
    report = generate_report(stats, len(data))

    filename = "REPORT_MULTILINGUAL.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ Report generated: {filename}")

if __name__ == '__main__':
    main()
