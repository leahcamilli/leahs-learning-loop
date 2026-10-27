---
title: "J-Space: A Geometric View of How Neural Networks Organize Knowledge"
source: "https://youtu.be/bjHuGNo3spk?is=Uy40_ykoAFJdKF0b"
date: "2026-07-09"
tags: [machine-learning, representation-learning, neural-networks, geometry, interpretability]
source_type: "youtube"
channel: "Matthew Berman"
published: "2026-07-07"
duration_seconds: 1534
kind: "deep-dive"
depth: 2
actionability: 2
---

## TL;DR

> J-Space treats a neural network’s internal representations as a high-dimensional geometry in which useful concepts and decisions become easier to separate. This matters because engineers can analyze that geometry to debug models, compare layers, and test what information a model has learned.

## Key Takeaways

1. Analyze clusters, directions, and subspaces in activations instead of assuming individual neurons correspond to individual concepts.
2. Compare raw inputs, hidden-layer activations, and final representations with linear probes to test whether task-relevant concepts become easier to separate.
3. Collect layer activations, visualize them with PCA or UMAP, and measure their structure with cosine or Euclidean distance.
4. Treat each neural-network layer as a transformation that can separate relevant features while compressing nuisance variation.
5. Do not infer model behavior from a probe alone: a probe can detect encoded information without proving the model uses that information to make decisions.
6. Interpret 2D projections cautiously because PCA, t-SNE, and UMAP can obscure or distort the original high-dimensional geometry.

## Overview

This lesson introduces the idea of "J-Space," a geometric framing for understanding how modern AI models may organize and process information internally. Rather than treating a neural network as an opaque function approximator, the central theme is that useful structure emerges in its learned representations: concepts, relationships, and decisions can often be understood as positions, directions, and transformations in a high-dimensional space.

Working engineers should care because this perspective connects directly to practical tasks like feature design, embedding analysis, debugging model behavior, interpretability, and evaluation. If you build or use deep learning systems, understanding representations as geometry gives you a more actionable mental model than simply thinking in terms of layers and weights.

## Key Concepts

- **Representation space**: Neural networks transform raw inputs into internal vectors, often called embeddings or latent representations. These vectors live in high-dimensional spaces where similarity, clustering, and direction can correspond to meaningful semantic structure.
- **Geometry of concepts**: A learned model may encode concepts not as single neurons but as regions, axes, or subspaces within a representation space. This geometric view helps explain why interpolation, analogy-like behavior, and linear probes can work surprisingly well.
- **Transformation across layers**: Each layer in a neural network can be seen as reshaping the representation space. Early layers often preserve local input structure, while later layers progressively separate task-relevant features and compress nuisance variation.
- **Linear separability**: One way to judge whether a network has learned a useful internal representation is to ask whether downstream concepts become easy to separate with a simple classifier. If later-layer embeddings are more linearly separable, the model is organizing information into a more useful form.
- **Emergent structure**: Even when trained only on next-step prediction or classification, models can develop internal structure that reflects categories, syntax, semantics, or task-relevant abstractions. This is a key reason representation analysis is useful for understanding what a model has learned.
- **Interpretability through probes**: Instead of reading weights directly, practitioners often inspect learned spaces with tools such as PCA, t-SNE, cosine similarity, and linear probes. These methods do not fully explain a model, but they can reveal whether meaningful structure exists in the latent space.

## How It Works

The core idea is to replace the vague question "how does AI think?" with a more concrete one: **what structure exists in the model's internal representation space, and how is it transformed during computation?** In this framing, the model is not just a sequence of matrix multiplications; it is a machine that maps data into a geometry where useful decisions become easier.

A practical way to think about this is in three stages:

1. **Encode input into a latent vector**  
   Raw data such as text, images, or audio is mapped into a dense vector representation. This vector is already more structured than the raw input because the network has learned to preserve distinctions that matter to the training objective.

2. **Reshape the space through layers**  
   Each layer changes the geometry of the representation. Distances between examples may shrink or grow, clusters may become more distinct, and directions associated with important factors may become more aligned with the target task.

3. **Read out a decision or prediction**  
   By the final layers, the representation often makes the target easier to compute. A simple linear projection may be enough to produce a class label, next token distribution, or scalar prediction.

This lens helps explain why deep learning works well in domains where the raw input is messy but the underlying structure is regular. For example, in image classification, raw pixel space is a poor space for distinguishing semantic classes. But after enough learned transformations, examples of similar objects may cluster together, and decision boundaries can become comparatively simple.

A useful engineering interpretation of J-Space is that it emphasizes **structure over individual parameters**. Instead of asking whether neuron 1847 means "dog," you ask:

- Do dog-like examples cluster together?
- Is there a direction corresponding to pose, color, or texture?
- Does a simple probe recover breed, object identity, or scene category?
- How does that structure change from one layer to the next?

This is especially relevant in modern models where information is distributed across many units. Single-neuron explanations are often brittle, but geometric explanations can remain stable and measurable.

In practice, engineers study these spaces using a workflow like this:

- Collect activations from one or more layers for a dataset.
- Reduce dimensionality for visualization with PCA or UMAP.
- Measure pairwise similarities using cosine distance or Euclidean distance.
- Train linear probes to test whether specific attributes are encoded.
- Compare earlier and later layers to see where useful abstractions emerge.

For language models, the same logic applies. Tokens are embedded into vectors, contextual layers transform those vectors, and later representations often encode syntax, semantics, entity identity, or discourse state. The output head then converts this final representation into token probabilities. In this view, the model's apparent reasoning ability comes partly from how effectively it arranges and manipulates information in latent space.

There are also important caveats:

- Visualizations in 2D can be misleading because the real geometry is high-dimensional.
- Linear probes can detect information without proving the model actually uses it for decisions.
- Similarity metrics matter; cosine similarity and Euclidean distance can tell different stories.
- A clean geometric story is helpful, but it is still an approximation of a complex dynamical system.

Even with those limitations, the representation-space perspective is one of the most practical ways to connect theory with day-to-day model work. It supports debugging, model comparison, transfer learning, retrieval systems, and interpretability research because it turns hidden activations into something you can measure and reason about.

## Training Exercise

Build a small experiment that tests whether a neural network's hidden layers become more structured than its input space.

### Goal
Train a simple classifier and compare the geometry of:

1. raw input features
2. hidden-layer activations
3. final-layer activations

Then measure whether classes become easier to separate.

### Steps
1. Pick a simple dataset such as MNIST, Fashion-MNIST, or Iris.
2. Train a small MLP classifier.
3. Save activations from each hidden layer for a validation set.
4. Project raw inputs and activations into 2D using PCA.
5. Train a logistic regression probe on each representation.
6. Compare probe accuracy and visualize cluster structure.

### Example workflow
```python
import torch
import torch.nn as nn
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

class MLP(nn.Module):
    def __init__(self, d_in, d_hidden, d_out):
        super().__init__()
        self.fc1 = nn.Linear(d_in, d_hidden)
        self.fc2 = nn.Linear(d_hidden, d_hidden)
        self.fc3 = nn.Linear(d_hidden, d_out)
        self.act = nn.ReLU()

    def forward(self, x):
        h1 = self.act(self.fc1(x))
        h2 = self.act(self.fc2(h1))
        y = self.fc3(h2)
        return y, h1, h2
```

### What to record
- Classification accuracy of the full network
- Probe accuracy on raw inputs
- Probe accuracy on hidden layer 1
- Probe accuracy on hidden layer 2
- PCA plots for each representation

### Questions to answer
- Do examples from the same class cluster more tightly in deeper layers?
- Does a linear probe perform better on hidden representations than on raw inputs?
- Are some classes separated early while others require deeper layers?
- How sensitive are the results to hidden size or activation function?

### Stretch task
Repeat the experiment with embeddings from a pretrained language or vision model. Compare representations from multiple layers and see where task-relevant structure appears most clearly.

## Test Yourself

<details><summary>What does the J-Space perspective emphasize when analyzing a neural network?</summary>

It emphasizes the geometry of internal representations: where examples lie, how they cluster, which directions encode attributes, and how layers transform that structure. This shifts attention from individual parameters or neurons to measurable organization across many units.

</details>

<details><summary>How can an engineer test whether deeper layers produce more useful representations?</summary>

Extract activations from several layers, train the same simple linear probe on each representation, and compare validation accuracy. PCA or UMAP plots can supplement the measurement by showing how class clusters and boundaries change.

</details>

<details><summary>Why are linear probes and 2D visualizations insufficient as complete explanations of a model?</summary>

A probe may recover information that the model does not actually use, while a 2D projection can distort high-dimensional relationships. Both are diagnostic tools whose conclusions should be checked with additional metrics and behavioral evidence.

</details>

## Further Reading

- [Distill: Visualizing Representations](https://distill.pub/)
- [CS231n: Neural Networks Part 2](https://cs231n.github.io/neural-networks-2/)
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
- [OpenAI: Microscope](https://microscope.openai.com/)
