import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.decomposition import PCA
import warnings,os

warnings.filterwarnings('ignore')
from typing import List, Dict, Tuple, Any
import re
from collections import Counter
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import seaborn as sns
from kneed import KneeLocator
import re
from collections import Counter

def extractKey_simple(txtdesc):
    if not isinstance(txtdesc, str):
        return ""

    stop_words = {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
        'for', 'of', 'with', 'by', 'as', 'is', 'are', 'was', 'were',
        'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
        'did', 'will', 'would', 'shall', 'should', 'may', 'might',
        'must', 'can', 'could', 'i', 'me', 'my', 'myself', 'we', 'our',
        'ours', 'you', 'your', 'yours', 'he', 'him', 'his', 'she', 'her',
        'hers', 'it', 'its', 'they', 'them', 'their', 'what', 'which',
        'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is',
        'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
        'had', 'having', 'do', 'does', 'did', 'doing', 'would', 'should',
        'could', 'ought', 'i\'m', 'you\'re', 'he\'s', 'she\'s', 'it\'s',
        'we\'re', 'they\'re', 'i\'ve', 'you\'ve', 'we\'ve', 'they\'ve',
        'i\'d', 'you\'d', 'he\'d', 'she\'d', 'we\'d', 'they\'d', 'i\'ll',
        'you\'ll', 'he\'ll', 'she\'ll', 'we\'ll', 'they\'ll', 'isn\'t',
        'aren\'t', 'wasn\'t', 'weren\'t', 'hasn\'t', 'haven\'t', 'hadn\'t',
        'doesn\'t', 'don\'t', 'didn\'t', 'won\'t', 'wouldn\'t', 'shan\'t',
        'shouldn\'t', 'can\'t', 'cannot', 'couldn\'t', 'mustn\'t', 'let\'s',
        'that\'s', 'who\'s', 'what\'s', 'here\'s', 'there\'s', 'when\'s',
        'where\'s', 'why\'s', 'how\'s', 'too', 'very', 'also', 'just',
        'about', 'above', 'below', 'from', 'up', 'down', 'out', 'so',
        'then', 'than', 'more', 'less', 'few', 'many', 'much', 'some',
        'any', 'no', 'not', 'only', 'own', 'same', 'other', 'another',
        'such', 'like', 'as', 'well'
    }

    text = txtdesc.lower()
    text = re.sub(r'[^\w\s]', ' ', text)

    words = text.split()

    filtered_words = [
        word for word in words
        if word not in stop_words and len(word) > 2
    ]

    word_freq = Counter(filtered_words)

    most_common = word_freq.most_common(4)

    keywords_list = [word for word, _ in most_common]
    keywords = ' '.join(keywords_list)

    return keywords


class AdaptiveTextCluster:

    def __init__(self,
                 auto_cluster_method: str = 'silhouette',  # 'silhouette', 'gap', 'hierarchical', 'dbscan'
                 clustering_algorithm: str = 'kmeans',  # 'kmeans', 'hierarchical', 'dbscan'
                 min_clusters: int = 2,
                 max_clusters: int = 10,
                 vectorizer: str = 'tfidf',
                 max_features: int = 2000,
                 random_state: int = 42):

        self.auto_cluster_method = auto_cluster_method
        self.clustering_algorithm = clustering_algorithm
        self.min_clusters = min_clusters
        self.max_clusters = max_clusters
        self.vectorizer_type = vectorizer
        self.max_features = max_features
        self.random_state = random_state

        self.vectorizer = None
        self.cluster_model = None
        self.labels_ = None
        self.n_clusters_ = None
        self.embeddings_ = None

        self.silhouette_scores_ = []
        self.calinski_scores_ = []
        self.davies_scores_ = []
        self.gap_stats_ = []

        self.stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
            'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him',
            'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',
            'itself', 'they', 'them', 'their', 'theirs', 'themselves',
            'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
            'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
            'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
            'into', 'through', 'during', 'before', 'after', 'above', 'below',
            'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
            'under', 'again', 'further', 'then', 'once', 'here', 'there',
            'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
            'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
            'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's',
            't', 'can', 'will', 'just', 'don', 'should', 'now'
        }

    def preprocess_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""

        text = text.lower()

        text = re.sub(r'[^\w\s]', ' ', text)

        tokens = text.split()

        tokens = [token for token in tokens
                  if token not in self.stop_words and len(token) > 2]

        return ' '.join(tokens)

    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        processed_texts = [self.preprocess_text(text) for text in texts]

        if self.vectorizer_type == 'tfidf':
            self.vectorizer = TfidfVectorizer(
                max_features=self.max_features,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95
            )
            embeddings = self.vectorizer.fit_transform(processed_texts)
            embeddings = embeddings.toarray()

        if embeddings.shape[1] > 50:
            pca = PCA(n_components=min(50, embeddings.shape[0]),
                      random_state=self.random_state)
            embeddings = pca.fit_transform(embeddings)

        self.embeddings_ = embeddings
        return embeddings

    def evaluate_clusters_silhouette(self, embeddings: np.ndarray) -> int:

        n_samples = len(embeddings)
        max_clusters = min(self.max_clusters, n_samples - 1)

        silhouette_scores = []

        for n in range(self.min_clusters, max_clusters + 1):
            if n > n_samples - 1:
                break

            kmeans = KMeans(n_clusters=n, random_state=self.random_state, n_init=10)
            labels = kmeans.fit_predict(embeddings)

            if len(set(labels)) > 1:
                score = silhouette_score(embeddings, labels)
                silhouette_scores.append(score)
            else:
                silhouette_scores.append(0)

            print(f"  K={n}: factor = {silhouette_scores[-1]:.4f}")

        if silhouette_scores:

            best_idx = np.argmax(silhouette_scores)
            best_n = self.min_clusters + best_idx
            best_score = silhouette_scores[best_idx]

            print(f"best n cluster: K={best_n}, factor={best_score:.4f}")

            # 保存所有分数用于可视化
            self.silhouette_scores_ = silhouette_scores

            return best_n
        else:
            return 2

    def evaluate_clusters_gap(self, embeddings: np.ndarray) -> int:

        n_samples = len(embeddings)
        max_clusters = min(self.max_clusters, n_samples - 1)

        gaps = []
        sks = []

        n_refs = 10
        reference_dispersions = []

        for n in range(self.min_clusters, max_clusters + 1):
            if n > n_samples - 1:
                break

            kmeans = KMeans(n_clusters=n, random_state=self.random_state, n_init=10)
            labels = kmeans.fit_predict(embeddings)

            dispersion = 0
            for i in range(n):
                cluster_points = embeddings[labels == i]
                if len(cluster_points) > 0:
                    centroid = np.mean(cluster_points, axis=0)
                    dispersion += np.sum(np.linalg.norm(cluster_points - centroid, axis=1))

            ref_dispersions = []
            for ref in range(n_refs):
                random_data = np.random.random_sample(embeddings.shape)
                kmeans_ref = KMeans(n_clusters=n, random_state=self.random_state, n_init=5)
                labels_ref = kmeans_ref.fit_predict(random_data)

                ref_dispersion = 0
                for i in range(n):
                    cluster_points = random_data[labels_ref == i]
                    if len(cluster_points) > 0:
                        centroid = np.mean(cluster_points, axis=0)
                        ref_dispersion += np.sum(np.linalg.norm(cluster_points - centroid, axis=1))

                ref_dispersions.append(np.log(ref_dispersion))

            gap = np.mean(ref_dispersions) - np.log(dispersion)
            gaps.append(gap)

            sk = np.sqrt(1 + 1 / n_refs) * np.std(ref_dispersions)
            sks.append(sk)

            print(f"  K={n}: Gap={gaps[-1]:.4f}, Standard Deviation={sks[-1]:.4f}")

        if gaps:

            best_n = self.min_clusters
            for i in range(len(gaps) - 1):
                if gaps[i] >= gaps[i + 1] - sks[i + 1]:
                    best_n = self.min_clusters + i
                    break

            print(f"best n cluster: K={best_n}, Gap Statistic={gaps[best_n - self.min_clusters]:.4f}")

            self.gap_stats_ = gaps

            return best_n
        else:
            return 2

    def evaluate_clusters_hierarchical(self, embeddings: np.ndarray) -> int:

        n_samples = len(embeddings)

        if n_samples > 1000:
            indices = np.random.choice(n_samples, size=min(1000, n_samples), replace=False)
            sample_embeddings = embeddings[indices]
        else:
            sample_embeddings = embeddings

        Z = linkage(sample_embeddings, method='ward', metric='euclidean')

        last_height = 0
        max_gap = 0
        best_cut = 2

        for i in range(1, len(Z)):
            height = Z[-i, 2]
            gap = height - last_height

            if gap > max_gap and i <= self.max_clusters:
                max_gap = gap
                best_cut = i + 1

            last_height = height

            if i >= self.max_clusters:
                break

        print(f"Suggested Number of Clusters in Hierarchical Clustering: K={best_cut}")
        return min(best_cut, n_samples - 1)

    def auto_determine_clusters(self, embeddings: np.ndarray) -> int:
        n_samples = len(embeddings)

        if n_samples < 3:
            return 1

        if self.min_clusters >= n_samples:
            return max(1, n_samples - 1)

        if self.auto_cluster_method == 'silhouette':
            return self.evaluate_clusters_silhouette(embeddings)
        elif self.auto_cluster_method == 'gap':
            return self.evaluate_clusters_gap(embeddings)
        elif self.auto_cluster_method == 'hierarchical':
            return self.evaluate_clusters_hierarchical(embeddings)
        elif self.auto_cluster_method == 'dbscan':
            return -1
        else:
            return self.evaluate_clusters_silhouette(embeddings)

    def cluster_with_kmeans(self, embeddings: np.ndarray, n_clusters: int) -> np.ndarray:
        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=self.random_state,
            n_init=20
        )
        labels = kmeans.fit_predict(embeddings)
        self.cluster_model = kmeans
        return labels

    def cluster_with_hierarchical(self, embeddings: np.ndarray, n_clusters: int) -> np.ndarray:
        hierarchical = AgglomerativeClustering(
            n_clusters=n_clusters,
            linkage='ward',
            metric='euclidean'
        )
        labels = hierarchical.fit_predict(embeddings)
        self.cluster_model = hierarchical
        return labels

    def cluster_with_dbscan(self, embeddings: np.ndarray) -> np.ndarray:
        print("Automatic Cluster Discovery Using DBSCAN...")

        from sklearn.neighbors import NearestNeighbors

        neighbors = NearestNeighbors(n_neighbors=5)
        neighbors_fit = neighbors.fit(embeddings)
        distances, indices = neighbors_fit.kneighbors(embeddings)
        distances = np.sort(distances[:, 4], axis=0)

        #from kneed import KneeLocator

        x = range(len(distances))
        kneedle = KneeLocator(x, distances, curve='convex', direction='increasing')

        if kneedle.elbow:
            eps = distances[kneedle.elbow]
        else:
            eps = 0.5

        print(f"DBSCAN parameter: eps={eps:.3f}, min_samples=5")

        dbscan = DBSCAN(eps=eps, min_samples=5)
        labels = dbscan.fit_predict(embeddings)
        self.cluster_model = dbscan

        unique_labels = set(labels)
        n_clusters = len([l for l in unique_labels if l != -1])
        noise_count = np.sum(labels == -1)

        print(f"DBSCAN found {n_clusters} cluster, Noise: {noise_count}")

        return labels

    def generate_cluster_description(self, cluster_texts: List[str]) -> str:
        if not cluster_texts:
            return "Empty_Cluster"

        all_words = []
        for text in cluster_texts:
            tokens = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            tokens = [t for t in tokens if t not in self.stop_words]
            all_words.extend(tokens)

        if not all_words:
            return "General_Solutions"

        word_counts = Counter(all_words)

        common_words = [word for word, count in word_counts.most_common(5)]

        representative_phrases = []
        for text in cluster_texts[:5]:
            sentences = re.split(r'[.!?]', text)
            for sentence in sentences:
                if len(sentence.split()) >= 3 and len(sentence.split()) <= 10:
                    if any(word in sentence.lower() for word in common_words[:3]):
                        representative_phrases.append(sentence.strip())
                        break

        if representative_phrases:
            description = min(representative_phrases, key=lambda x: len(x))
        else:
            description = f"{' '.join(common_words[:3])}"

        description = re.sub(r'\s+', ' ', description.strip())
        #description = description[:100]
        description = extractKey_simple(description)

        return description

    def cluster(self, texts: List[str]) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
        if not texts or len(texts) < 2:
            return {}, {}

        print("=" * 60)
        print(f"length of texts: {len(texts)}")
        print(f"automatic cluster: {self.auto_cluster_method}")
        print(f"method: {self.clustering_algorithm}")

        print("\n1. create vector...")
        embeddings = self.create_embeddings(texts)
        print(f"   Dimensionality: {embeddings.shape}")

        print("\n2. best n cluster...")
        n_clusters = self.auto_determine_clusters(embeddings)
        self.n_clusters_ = n_clusters

        if n_clusters == -1:
            # DBSCAN
            print("3. Automatic find cluster by DBSCAN...")
            labels = self.cluster_with_dbscan(embeddings)
        else:
            print(f"3.  (K={n_clusters}) ...")

            if self.clustering_algorithm == 'kmeans':
                labels = self.cluster_with_kmeans(embeddings, n_clusters)
            elif self.clustering_algorithm == 'hierarchical':
                labels = self.cluster_with_hierarchical(embeddings, n_clusters)
            else:
                labels = self.cluster_with_kmeans(embeddings, n_clusters)

        print("\n4. generate description...")
        unique_labels = np.unique(labels)

        dict_solution = {}
        dict_count = {}

        for label in unique_labels:
            if label == -1:
                cluster_name = "Noise_Outliers"
            else:
                cluster_indices = np.where(labels == label)[0]
                cluster_texts_list = [texts[i] for i in cluster_indices]

                cluster_name = self.generate_cluster_description(cluster_texts_list)

                base_name = cluster_name
                counter = 1
                while cluster_name in dict_solution:
                    cluster_name = f"{base_name}_{counter}"
                    counter += 1

                dict_solution[cluster_name] = cluster_texts_list
                dict_count[cluster_name] = len(cluster_texts_list)

        if len(set(labels)) > 1 and -1 not in set(labels):
            try:
                silhouette = silhouette_score(embeddings, labels)
                calinski = calinski_harabasz_score(embeddings, labels)
                davies = davies_bouldin_score(embeddings, labels)

            except:
                pass

        # 保存标签
        self.labels_ = labels

        return dict_solution, dict_count

    def visualize_clustering(self, texts: List[str], save_path: str = None):
        if self.embeddings_ is None or self.labels_ is None:
            return

        try:
            import matplotlib.pyplot as plt
            from sklearn.manifold import TSNE

            print("generate chart...")

            tsne = TSNE(n_components=2, random_state=self.random_state)
            embeddings_2d = tsne.fit_transform(self.embeddings_)

            fig, axes = plt.subplots(2, 2, figsize=(14, 10))

            unique_labels = np.unique(self.labels_)
            colors = plt.cm.Set3(np.linspace(0, 1, len(unique_labels)))

            for i, label in enumerate(unique_labels):
                if label == -1:
                    color = 'gray'
                    label_name = 'Noise'
                else:
                    color = colors[i]
                    label_name = f'Cluster {label}'

                mask = self.labels_ == label
                axes[0, 0].scatter(
                    embeddings_2d[mask, 0],
                    embeddings_2d[mask, 1],
                    c=[color],
                    label=label_name,
                    alpha=0.7,
                    s=30
                )

            axes[0, 0].set_title('t-SNE visualization')
            axes[0, 0].set_xlabel('t-SNE 1')
            axes[0, 0].set_ylabel('t-SNE 2')
            axes[0, 0].legend(loc='best')
            axes[0, 0].grid(True, alpha=0.3)

            if hasattr(self, 'n_clusters_') and self.n_clusters_ > 0:
                cluster_sizes = []
                cluster_names = []

                for label in unique_labels:
                    if label != -1:
                        size = np.sum(self.labels_ == label)
                        cluster_sizes.append(size)
                        cluster_names.append(f'Cluster {label}')

                if cluster_sizes:
                    axes[0, 1].bar(range(len(cluster_sizes)), cluster_sizes)
                    axes[0, 1].set_xticks(range(len(cluster_sizes)))
                    axes[0, 1].set_xticklabels(cluster_names, rotation=45, ha='right')
                    axes[0, 1].set_title('Cluster Size Distribution')
                    axes[0, 1].set_ylabel('Number of Instances')
                    axes[0, 1].grid(True, alpha=0.3, axis='y')

            # 3. 轮廓系数图（如果有）
            if hasattr(self, 'silhouette_scores_') and self.silhouette_scores_:
                k_values = list(range(self.min_clusters,
                                      self.min_clusters + len(self.silhouette_scores_)))
                axes[1, 0].plot(k_values, self.silhouette_scores_, 'bo-')
                axes[1, 0].set_xlabel('Number of Clusters (K)')
                axes[1, 0].set_ylabel('Silhouette Coefficient')
                axes[1, 0].set_title('Silhouette Coefficient vs Number of Clusters')
                axes[1, 0].grid(True, alpha=0.3)

                if len(self.silhouette_scores_) > 0:
                    best_idx = np.argmax(self.silhouette_scores_)
                    best_k = k_values[best_idx]
                    best_score = self.silhouette_scores_[best_idx]
                    axes[1, 0].plot(best_k, best_score, 'ro', markersize=10)

            axes[1, 1].text(0.5, 0.5, 'Cluster Statistics',
                            ha='center', va='center', fontsize=12)
            axes[1, 1].axis('off')

            if self.n_clusters_ and self.n_clusters_ > 0:
                info_text = f"Number of clusters: {self.n_clusters_}\n"
                info_text += f"Total samples: {len(texts)}\n"

                if -1 in self.labels_:
                    noise_count = np.sum(self.labels_ == -1)
                    info_text += f"Noise points: {noise_count}\n"

                axes[1, 1].text(0.5, 0.4, info_text,
                                ha='center', va='center', fontsize=10)

            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"Visualization chart saved to: {save_path}")

            plt.show()


        except ImportError as e:
            print(f"Visualization requires matplotlib and scikit-learn: {e}")
        except Exception as e:
            print(f"Error occurred during visualization: {e}")


def adaptive_text_clustering_from_excel(
        excel_path: str,
        text_column: str = None,
        auto_cluster_method: str = 'silhouette',
        clustering_algorithm: str = 'kmeans',
        min_clusters: int = 2,
        max_clusters: int = 10,
        sheet_name: int = 0,
        visualize: bool = True
) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
    print(f"Reading Excel file: {excel_path}")
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        print(f"File read successfully, shape: {df.shape}")

        if text_column is None or text_column not in df.columns:
            for col in df.columns:
                if df[col].dtype == 'object':
                    text_column = col
                    print(f"Using column '{text_column}' as the text column")
                    break

            if text_column is None:
                raise ValueError("No suitable text column found")

        texts = df[text_column].dropna().astype(str).tolist()
        print(f"Extracted {len(texts)} texts")

        if len(texts) < 2:
            print("Insufficient number of texts for clustering")
            return {}, {}

        clusterer = AdaptiveTextCluster(
            auto_cluster_method=auto_cluster_method,
            clustering_algorithm=clustering_algorithm,
            min_clusters=min_clusters,
            max_clusters=min(max_clusters, len(texts) - 1),
            random_state=42
        )

        dict_solution, dict_count = clusterer.cluster(texts)

        total_samples = sum(dict_count.values())
        for cluster_desc, count in dict_count.items():
            percentage = (count / total_samples) * 100
            print(f"  {cluster_desc}: {count} samples ({percentage:.1f}%)")
        '''
        if visualize and len(texts) > 2:
            clusterer.visualize_clustering(texts, "clustering_visualization.png")
        '''
        return dict_solution, dict_count

    except Exception as e:
        print(f"error in excel: {str(e)}")
        import traceback
        traceback.print_exc()
        return {}, {}

def quick_adaptive_cluster(
        file_path: str,
        text_col: str = None,
        method: str = 'silhouette',
        min_k: int = 2,
        max_k: int = 10
):

    return adaptive_text_clustering_from_excel(
        excel_path=file_path,
        text_column=text_col,
        auto_cluster_method=method,
        min_clusters=min_k,
        max_clusters=max_k
    )


if __name__ == "__main__":
    # 配置参数
    fp = os.getcwd()
    for i in range(0,5):
        input_file = os.path.join(fp, f"./data/recommended_solutions_case{i}.xlsx")  # 您的Excel文件路径
        excel_path = input_file   # 您的Excel文件路径
        text_column = "Recommended Solutions"  # 文本列名
        output_path =os.path.join(fp,  f"./data/adaptive_clustering_results_case{i}.xlsx")  # 输出文件路径

        print("自适应文本聚类系统 - 不固定分类数")
        print("=" * 60)

        # 执行自适应聚类
        dict_solution, dict_count = adaptive_text_clustering_from_excel(
            excel_path=excel_path,
            text_column=text_column,
            auto_cluster_method='silhouette',  # 使用轮廓系数自动确定K
            clustering_algorithm='kmeans',
            min_clusters=2,
            max_clusters=15,
            visualize=True
        )

        # 输出结果
        print("\n" + "=" * 60)
        print("create dictionary")
        print("=" * 60)

        print("\n1. dict_solution structure:")
        for cluster_desc, texts in dict_solution.items():
            print(f"\n[{cluster_desc}] - {len(texts)} 个样本:")
            for i, text in enumerate(texts[:2]):  # 每个聚类显示前2个样本
                preview = text[:80] + "..." if len(text) > 80 else text
                print(f"  {i + 1}. {preview}")

        print("\n2. dict_count 内容:")
        for cluster_desc, count in dict_count.items():
            print(f"  {cluster_desc}: {count}")

        # 保存结果到Excel
        if dict_solution:
            output_data = []
            for cluster_desc, texts in dict_solution.items():
                for text in texts:
                    output_data.append({
                        'Cluster_Description': cluster_desc,
                        'Original_Text': text,
                        'Text_Length': len(text),
                        'Cluster_Size': len(texts)
                    })

            output_df = pd.DataFrame(output_data)
            output_df.to_excel(output_path, index=False)
            print(f"\nsave success: {output_path}")