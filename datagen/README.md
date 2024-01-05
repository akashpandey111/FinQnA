Fine-tuning is about adjusting the model weights to maximize performance on a narrowly defined specific task, for example, provide the best possible financial advice.

In a real-world project, we would hire a team of financial experts, to bootstrap an initial dataset of pairs (question, answer). In this tutorial, we will folow a semi-automatic approach, and use a general LLM, like ChatGPT, to bootstrap a reasonable training set.

This dataset should resemble as much as possible the actual questions, and answers we expect, from this model once deployed. This is the dataset we will use to **fine-tune** our LLM.