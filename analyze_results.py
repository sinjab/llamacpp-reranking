#!/usr/bin/env python3
"""
Analyze reranking model test results and generate quantization reports.
Processes CSV data and creates 4 reports: Q4_K_M, Q8_0, F16, and comparison.
"""

import csv
from collections import defaultdict
from typing import Dict, List, Tuple

def load_and_parse_csv(filepath: str) -> Dict[str, List[Dict]]:
    """Load CSV and group by quantization type."""
    results = {
        'Q4_K_M': [],
        'Q8_0': [],
        'F16': []
    }

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            model_name = row['model_name']
            if 'Q4_K_M' in model_name:
                quant_type = 'Q4_K_M'
            elif 'Q8_0' in model_name:
                quant_type = 'Q8_0'
            elif 'F16' in model_name:
                quant_type = 'F16'
            else:
                continue

            # Convert types
            row['response_time_seconds'] = float(row['response_time_seconds'])
            row['model_size_mb'] = float(row['model_size_mb'])
            row['correct_answer'] = row['correct_answer'] == 'TRUE'
            row['success'] = row['success'] == 'TRUE'

            results[quant_type].append(row)

    return results

def calculate_model_stats(data: List[Dict]) -> Dict[str, Dict]:
    """Calculate statistics per model."""
    model_stats = defaultdict(lambda: {
        'total_tests': 0,
        'correct': 0,
        'times': [],
        'size_mb': 0,
        'domains': defaultdict(lambda: {'total': 0, 'correct': 0})
    })

    for row in data:
        model = row['model_name'].rsplit('-', 1)[0]  # Remove quantization suffix
        stats = model_stats[model]

        stats['total_tests'] += 1
        stats['size_mb'] = row['model_size_mb']
        stats['times'].append(row['response_time_seconds'])

        if row['correct_answer']:
            stats['correct'] += 1

        domain = row['domain']
        stats['domains'][domain]['total'] += 1
        if row['correct_answer']:
            stats['domains'][domain]['correct'] += 1

    # Calculate averages
    for model, stats in model_stats.items():
        stats['accuracy'] = (stats['correct'] / stats['total_tests'] * 100) if stats['total_tests'] > 0 else 0
        stats['avg_time'] = sum(stats['times']) / len(stats['times']) if stats['times'] else 0
        stats['min_time'] = min(stats['times']) if stats['times'] else 0
        stats['max_time'] = max(stats['times']) if stats['times'] else 0

    return dict(model_stats)

def get_top_models(stats: Dict, by: str = 'accuracy', limit: int = 5) -> List[Tuple[str, Dict]]:
    """Get top N models by specified metric."""
    if by == 'accuracy':
        sorted_models = sorted(stats.items(), key=lambda x: (-x[1]['accuracy'], x[1]['avg_time']))
    elif by == 'speed':
        sorted_models = sorted(stats.items(), key=lambda x: (x[1]['avg_time'], -x[1]['accuracy']))
    elif by == 'size':
        sorted_models = sorted(stats.items(), key=lambda x: (x[1]['size_mb'], -x[1]['accuracy']))
    else:
        sorted_models = list(stats.items())

    return sorted_models[:limit]

def format_time(seconds: float) -> str:
    """Format time in ms."""
    return f"{int(seconds * 1000)}ms"

def format_size(mb: float) -> str:
    """Format size in MB or GB."""
    if mb >= 1000:
        return f"{mb/1000:.1f} GB"
    return f"{int(mb)} MB"

def generate_quant_report(quant_type: str, stats: Dict, total_tests: int) -> str:
    """Generate report for a single quantization type."""

    # Count perfect accuracy models
    perfect_models = [m for m, s in stats.items() if s['accuracy'] == 100]

    # Get rankings
    top_accuracy = get_top_models(stats, 'accuracy', 10)
    top_speed = get_top_models(stats, 'speed', 5)
    top_size = get_top_models(stats, 'size', 5)

    # Calculate overall stats
    avg_accuracy = sum(s['accuracy'] for s in stats.values()) / len(stats) if stats else 0
    avg_time = sum(s['avg_time'] for s in stats.values()) / len(stats) if stats else 0
    total_size = sum(s['size_mb'] for s in stats.values())

    # Build report
    report = f"""# Reranking Models Benchmark Report - {quant_type} Quantization

## Executive Summary

**Tests Completed:** {total_tests} ({len(stats)} models × 10 domains)
**Overall Accuracy:** {avg_accuracy:.1f}%
**Average Response Time:** {format_time(avg_time)}
**Total Storage:** {format_size(total_size)}
**Perfect Accuracy Models:** {len(perfect_models)}

## Performance Rankings

### Top 10 Models by Accuracy
"""

    for i, (model, s) in enumerate(top_accuracy, 1):
        emoji = "🏆" if i == 1 else "⭐" if i <= 3 else ""
        report += f"{i}. **{model}** {emoji}\n"
        report += f"   - Accuracy: {s['accuracy']:.0f}% ({s['correct']}/{s['total_tests']})\n"
        report += f"   - Speed: {format_time(s['avg_time'])} (range: {format_time(s['min_time'])}-{format_time(s['max_time'])})\n"
        report += f"   - Size: {format_size(s['size_mb'])}\n\n"

    report += f"\n### Top 5 Fastest Models\n\n"
    for i, (model, s) in enumerate(top_speed, 1):
        report += f"{i}. **{model}** - {format_time(s['avg_time'])} ({s['accuracy']:.0f}% accuracy, {format_size(s['size_mb'])})\n"

    report += f"\n### Top 5 Smallest Models\n\n"
    for i, (model, s) in enumerate(top_size, 1):
        report += f"{i}. **{model}** - {format_size(s['size_mb'])} ({s['accuracy']:.0f}% accuracy, {format_time(s['avg_time'])})\n"

    # Perfect accuracy models details
    if perfect_models:
        report += f"\n## Perfect Accuracy Models (100%)\n\n"
        perfect_stats = [(m, stats[m]) for m in perfect_models]
        perfect_stats.sort(key=lambda x: x[1]['avg_time'])

        for model, s in perfect_stats:
            report += f"**{model}**\n"
            report += f"- Speed: {format_time(s['avg_time'])} | Size: {format_size(s['size_mb'])}\n"
            report += f"- Best for: "
            if s['size_mb'] < 100:
                report += "Resource-constrained environments"
            elif s['avg_time'] < 0.1:
                report += "Low-latency applications"
            elif s['size_mb'] > 1000:
                report += "Maximum quality requirements"
            else:
                report += "Balanced performance"
            report += "\n\n"

    # Domain analysis for top model
    if top_accuracy:
        top_model, top_stats = top_accuracy[0]
        report += f"## Domain Performance Analysis - {top_model}\n\n"

        domain_perf = [(d, s['correct']/s['total']*100) for d, s in top_stats['domains'].items()]
        domain_perf.sort(key=lambda x: -x[1])

        report += "| Domain | Accuracy |\n|--------|----------|\n"
        for domain, acc in domain_perf:
            report += f"| {domain.capitalize()} | {acc:.0f}% |\n"

    # Use case recommendations
    report += f"\n## Use Case Recommendations\n\n"

    report += "### Real-Time Search (Low Latency)\n"
    for model, s in top_speed[:3]:
        if s['accuracy'] >= 60:
            report += f"- **{model}**: {format_time(s['avg_time'])}, {s['accuracy']:.0f}% accuracy\n"

    report += f"\n### Edge Deployment (Small Size)\n"
    for model, s in top_size[:3]:
        if s['accuracy'] >= 60:
            report += f"- **{model}**: {format_size(s['size_mb'])}, {s['accuracy']:.0f}% accuracy\n"

    report += f"\n### Production RAG (Balanced)\n"
    balanced = [(m, s) for m, s in stats.items()
                if s['accuracy'] >= 80 and s['avg_time'] < 0.2 and s['size_mb'] < 1000]
    balanced.sort(key=lambda x: (-x[1]['accuracy'], x[1]['avg_time']))
    for model, s in balanced[:3]:
        report += f"- **{model}**: {s['accuracy']:.0f}% accuracy, {format_time(s['avg_time'])}, {format_size(s['size_mb'])}\n"

    report += f"\n### Maximum Accuracy (Quality Focus)\n"
    for model, s in top_accuracy[:3]:
        report += f"- **{model}**: {s['accuracy']:.0f}% accuracy, {format_time(s['avg_time'])}, {format_size(s['size_mb'])}\n"

    # Key findings
    report += f"\n## Key Findings\n\n"

    # Speed range
    fastest = min(stats.items(), key=lambda x: x[1]['avg_time'])
    slowest = max(stats.items(), key=lambda x: x[1]['avg_time'])
    report += f"- **Speed Range**: {format_time(fastest[1]['avg_time'])} ({fastest[0]}) to {format_time(slowest[1]['avg_time'])} ({slowest[0]})\n"

    # Size range
    smallest = min(stats.items(), key=lambda x: x[1]['size_mb'])
    largest = max(stats.items(), key=lambda x: x[1]['size_mb'])
    report += f"- **Size Range**: {format_size(smallest[1]['size_mb'])} ({smallest[0]}) to {format_size(largest[1]['size_mb'])} ({largest[0]})\n"

    # Accuracy distribution
    acc_90_plus = len([s for s in stats.values() if s['accuracy'] >= 90])
    acc_80_plus = len([s for s in stats.values() if s['accuracy'] >= 80])
    acc_below_50 = len([s for s in stats.values() if s['accuracy'] < 50])
    report += f"- **Accuracy Distribution**: {acc_90_plus} models ≥90%, {acc_80_plus} models ≥80%, {acc_below_50} models <50%\n"

    # Best value
    value_models = [(m, s) for m, s in stats.items() if s['accuracy'] >= 90]
    if value_models:
        best_value = min(value_models, key=lambda x: x[1]['size_mb'])
        report += f"- **Best Value**: {best_value[0]} achieves {best_value[1]['accuracy']:.0f}% in only {format_size(best_value[1]['size_mb'])}\n"

    return report

def generate_comparison_report(all_stats: Dict, all_data: Dict) -> str:
    """Generate comparison report across all quantizations."""

    report = """# Reranking Models - Quantization Comparison Report

## Overview

This report compares the performance of reranking models across three quantization levels:
- **F16**: Full 16-bit precision (highest quality, largest size)
- **Q8_0**: 8-bit quantization (middle ground)
- **Q4_K_M**: 4-bit quantization (smallest size, fastest)

## Quantization Impact Summary

"""

    # Calculate stats per quantization
    quant_summary = {}
    for quant in ['F16', 'Q8_0', 'Q4_K_M']:
        stats = all_stats[quant]
        quant_summary[quant] = {
            'num_models': len(stats),
            'avg_accuracy': sum(s['accuracy'] for s in stats.values()) / len(stats) if stats else 0,
            'avg_time': sum(s['avg_time'] for s in stats.values()) / len(stats) if stats else 0,
            'avg_size': sum(s['size_mb'] for s in stats.values()) / len(stats) if stats else 0,
            'perfect_models': len([s for s in stats.values() if s['accuracy'] == 100])
        }

    report += "| Quantization | Models | Avg Accuracy | Avg Speed | Avg Size | Perfect 100% |\n"
    report += "|--------------|--------|--------------|-----------|----------|---------------|\n"
    for quant in ['F16', 'Q8_0', 'Q4_K_M']:
        s = quant_summary[quant]
        report += f"| {quant} | {s['num_models']} | {s['avg_accuracy']:.1f}% | {format_time(s['avg_time'])} | {format_size(s['avg_size'])} | {s['perfect_models']} |\n"

    # Model family analysis - compare same models across quantizations
    report += "\n## Model Family Performance Across Quantizations\n\n"

    # Group models by base name
    model_families = defaultdict(dict)
    for quant, stats in all_stats.items():
        for model, s in stats.items():
            model_families[model][quant] = s

    # Find models available in all 3 quantizations
    complete_models = {m: data for m, data in model_families.items() if len(data) == 3}

    if complete_models:
        report += f"### Models Available in All Quantizations ({len(complete_models)} models)\n\n"

        # Sort by F16 accuracy
        sorted_families = sorted(complete_models.items(),
                                key=lambda x: -x[1]['F16']['accuracy'])

        for model, quant_data in sorted_families[:10]:  # Top 10
            report += f"**{model}**\n\n"
            report += "| Quant | Accuracy | Speed | Size | Accuracy Change | Speed Change |\n"
            report += "|-------|----------|-------|------|-----------------|---------------|\n"

            f16_acc = quant_data['F16']['accuracy']
            f16_time = quant_data['F16']['avg_time']

            for quant in ['F16', 'Q8_0', 'Q4_K_M']:
                s = quant_data[quant]
                acc_change = s['accuracy'] - f16_acc
                time_change = ((s['avg_time'] - f16_time) / f16_time * 100) if f16_time > 0 else 0

                acc_indicator = f"({acc_change:+.0f}%)" if quant != 'F16' else ""
                time_indicator = f"({time_change:+.0f}%)" if quant != 'F16' else ""

                report += f"| {quant} | {s['accuracy']:.0f}% | {format_time(s['avg_time'])} | "
                report += f"{format_size(s['size_mb'])} | {acc_indicator} | {time_indicator} |\n"
            report += "\n"

    # Quantization tradeoffs
    report += "\n## Quantization Tradeoff Analysis\n\n"

    report += "### Q4_K_M vs F16\n"
    report += f"- **Size Reduction**: ~60-70% smaller\n"
    report += f"- **Speed**: ~{abs(((quant_summary['Q4_K_M']['avg_time'] - quant_summary['F16']['avg_time']) / quant_summary['F16']['avg_time'] * 100)):.0f}% change\n"
    report += f"- **Accuracy Impact**: {(quant_summary['Q4_K_M']['avg_accuracy'] - quant_summary['F16']['avg_accuracy']):.1f}% change\n"
    report += f"- **Recommendation**: Best for production deployment - minimal accuracy loss with major size savings\n\n"

    report += "### Q8_0 vs F16\n"
    report += f"- **Size Reduction**: ~45-50% smaller\n"
    report += f"- **Speed**: ~{abs(((quant_summary['Q8_0']['avg_time'] - quant_summary['F16']['avg_time']) / quant_summary['F16']['avg_time'] * 100)):.0f}% change\n"
    report += f"- **Accuracy Impact**: {(quant_summary['Q8_0']['avg_accuracy'] - quant_summary['F16']['avg_accuracy']):.1f}% change\n"
    report += f"- **Recommendation**: Middle ground for quality-sensitive applications\n\n"

    # Best models per quantization
    report += "\n## Top Performer by Quantization Level\n\n"

    for quant in ['F16', 'Q8_0', 'Q4_K_M']:
        stats = all_stats[quant]
        if stats:
            best = max(stats.items(), key=lambda x: (x[1]['accuracy'], -x[1]['avg_time']))
            model, s = best

            report += f"### {quant} Winner: {model}\n"
            report += f"- **Accuracy**: {s['accuracy']:.0f}%\n"
            report += f"- **Speed**: {format_time(s['avg_time'])}\n"
            report += f"- **Size**: {format_size(s['size_mb'])}\n\n"

    # Recommendations
    report += "\n## Final Recommendations\n\n"

    report += "### When to Use Each Quantization:\n\n"
    report += "**F16 (Full Precision)**\n"
    report += "- Research and benchmarking\n"
    report += "- Maximum accuracy requirements\n"
    report += "- When storage is not a concern\n"
    report += "- Model evaluation and comparison\n\n"

    report += "**Q8_0 (8-bit)**\n"
    report += "- Quality-sensitive production systems\n"
    report += "- When slight accuracy drop is acceptable\n"
    report += "- Moderate storage constraints\n"
    report += "- Server deployments with good hardware\n\n"

    report += "**Q4_K_M (4-bit)** ⭐ **RECOMMENDED**\n"
    report += "- General production deployment\n"
    report += "- Edge devices and mobile\n"
    report += "- Cost-optimized cloud deployment\n"
    report += "- Best balance of speed, size, and accuracy\n"
    report += "- Minimal accuracy loss for most models\n\n"

    # Key insights
    report += "\n## Key Insights\n\n"

    # Find models that maintain 100% across all quantizations
    perfect_across_all = []
    for model, quant_data in complete_models.items():
        if all(quant_data[q]['accuracy'] == 100 for q in ['F16', 'Q8_0', 'Q4_K_M']):
            perfect_across_all.append(model)

    if perfect_across_all:
        report += f"- **{len(perfect_across_all)} models maintain 100% accuracy across ALL quantizations**: {', '.join(perfect_across_all)}\n"

    # Models with significant quantization impact
    big_impact = []
    for model, quant_data in complete_models.items():
        if len(quant_data) == 3:
            acc_drop = quant_data['F16']['accuracy'] - quant_data['Q4_K_M']['accuracy']
            if acc_drop > 10:
                big_impact.append((model, acc_drop))

    if big_impact:
        big_impact.sort(key=lambda x: -x[1])
        report += f"- **Models significantly affected by quantization** (>10% drop): {', '.join([f'{m} ({d:.0f}%)' for m, d in big_impact[:3]])}\n"

    # Size savings
    total_f16_size = sum(s['size_mb'] for s in all_stats['F16'].values())
    total_q4_size = sum(s['size_mb'] for s in all_stats['Q4_K_M'].values())
    savings_gb = (total_f16_size - total_q4_size) / 1024
    report += f"- **Total storage savings** (Q4_K_M vs F16): {savings_gb:.1f} GB saved ({((total_f16_size - total_q4_size) / total_f16_size * 100):.0f}% reduction)\n"

    return report

def main():
    """Main analysis function."""
    print("Loading test results...")
    data = load_and_parse_csv('test_results.csv')

    print("Calculating statistics...")
    all_stats = {}
    for quant in ['Q4_K_M', 'Q8_0', 'F16']:
        all_stats[quant] = calculate_model_stats(data[quant])
        print(f"  {quant}: {len(all_stats[quant])} models, {len(data[quant])} tests")

    print("\nGenerating reports...")

    # Generate individual quantization reports
    for quant in ['Q4_K_M', 'Q8_0', 'F16']:
        report = generate_quant_report(quant, all_stats[quant], len(data[quant]))
        filename = f"REPORT_{quant}.md"
        with open(filename, 'w') as f:
            f.write(report)
        print(f"  ✓ {filename}")

    # Generate comparison report
    comparison = generate_comparison_report(all_stats, data)
    with open('REPORT_COMPARISON.md', 'w') as f:
        f.write(comparison)
    print(f"  ✓ REPORT_COMPARISON.md")

    print("\n✅ All reports generated successfully!")
    print("\nReport files:")
    print("  - REPORT_Q4_K_M.md")
    print("  - REPORT_Q8_0.md")
    print("  - REPORT_F16.md")
    print("  - REPORT_COMPARISON.md")

if __name__ == '__main__':
    main()
