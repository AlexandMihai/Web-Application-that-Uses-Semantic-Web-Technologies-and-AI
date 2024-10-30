import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filepath):
    return pd.read_csv(filepath)

def compute_statistics(data, columns):
    summary_stats = data[columns].describe()
    return summary_stats

def plot_metrics(data, columns, title_prefix):
    plt.figure(figsize=(10, 6))
    for col in columns:
        plt.plot(data['Iteration'], data[col], label=col)
    plt.title(f'{title_prefix} Over Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_entity_metrics(data, entity_prefix):
    # Extracting columns for the specific entity
    entity_metrics = [col for col in data.columns if col.startswith(entity_prefix)]
    plt.figure(figsize=(12, 7))
    for metric in entity_metrics:
        plt.plot(data['Iteration'], data[metric], label=metric.split()[-1])  # Split to get P, R, F
    plt.title(f'Performance Metrics for {entity_prefix}')
    plt.xlabel('Iteration')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    filepath = 'training_scores_detailed.csv'  # Path to the CSV file
    data = load_data(filepath)

    # Computing statistics for key overall metrics
    key_metrics = ['Loss', 'Token Acc', 'Token P', 'Token R', 'Token F']
    stats = compute_statistics(data, key_metrics)
    print('Statistical Summary for Key Metrics:\n', stats)

    plot_metrics(data, ['Loss'], 'Loss')
    plot_metrics(data, ['Token Acc'], 'Token Accuracy')
    plot_metrics(data, ['Token P', 'Token R', 'Token F'], 'Token Performance (Precision, Recall, F-Score)')

    # Entity specific metrics
    entities = set(col.rsplit(' ', 2)[0] for col in data.columns if ' P' in col)  # Detect entities
    for entity in entities:
        plot_entity_metrics(data, entity)

if __name__ == "__main__":
    main()
