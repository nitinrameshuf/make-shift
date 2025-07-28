def calculate_security_score(submetric_counts: dict, weighted_scores: dict) -> float:
    score = 100.0  # start from perfect score

    for category, weight in weighted_scores.items():
        category_penalty = 0.0

        if category == 'AWS_IOM':
            # example submetrics: 'Critical', 'High', 'Medium', 'Low'
            critical = submetric_counts.get('iom_critical', 0)
            high = submetric_counts.get('iom_high', 0)
            medium = submetric_counts.get('iom_medium', 0)
            low = submetric_counts.get('iom_low', 0)

            total_penalty = (critical * 1.0 + high * 0.7 + medium * 0.4 + low * 0.1)
            category_penalty = min(total_penalty, weight)  # normalize

        elif category == 'Error_Containers':
            image_pull = submetric_counts.get('error_image_pull', 0)
            push = submetric_counts.get('error_image_push', 0)
            schema = submetric_counts.get('error_unsupported_schema_version', 0)
            config = submetric_counts.get('error_missing_config', 0)

            total_penalty = image_pull + push + schema + config
            category_penalty = min(total_penalty * 1.0, weight)

        elif category == 'Unmanaged_Assets':
            count = submetric_counts.get('unmanaged_assets', 0)
            category_penalty = min(count * 1.5, weight)  # scale to weight

        # Add more elif blocks for each category

        # Deduct from score
        score -= category_penalty

    return round(max(score, 0), 2)
