---
title: "MarkItDown for LLM Ingestion Pipelines"
source: "https://github.com/microsoft/markitdown"
date: "2026-04-17"
tags: [python, markdown, llm, document-conversion, plugins]
source_type: "github"
topics: [python]
kind: "deep-dive"
depth: 3
actionability: 1
---

## TL;DR

> MarkItDown converts heterogeneous documents and media into structure-preserving Markdown, giving LLM ingestion pipelines a lightweight common format for chunking, indexing, retrieval, and prompting. Its stream-based converters, optional dependencies, and explicit plugins keep the core predictable while allowing OCR, transcription, and image captioning when needed.

## Key Takeaways

1. Use Markdown as an intermediate ingestion format when headings, lists, tables, and links matter more than pixel-perfect rendering.
2. Pass binary file-like streams to converters to avoid temporary files and support in-memory or service-based workflows.
3. Install optional extras only for required formats such as PDF, DOCX, PPTX, XLSX, and audio to keep deployments smaller and modular.
4. Layer OpenAI-compatible image captioning, Azure Document Intelligence, OCR, or transcription on top of deterministic conversion only when conventional parsing is insufficient.
5. Enable separately packaged plugins explicitly to add or override converters without modifying the core library.
6. Study the dedicated Office, PDF, archive, image, audio, and notebook converters when designing dispatch for heterogeneous document pipelines.
7. Include external tools such as `ffmpeg` and `exiftool` in container images when media conversion requires them.

## Overview

These notes cover **MarkItDown**, a Python framework for converting many file and media formats into structured Markdown for downstream use in LLM pipelines, search, retrieval, and text analysis. The key idea is that Markdown is a practical intermediate format: it preserves useful structure like headings, lists, tables, and links without aiming for pixel-perfect rendering.

The repository is especially relevant for engineers building document ingestion systems. Beyond basic conversion, it demonstrates a solid architecture for stream-based processing, converter dispatch, optional dependency loading, plugin-based extension, and selective AI-assisted enrichment such as OCR, image captioning, and audio transcription.

## Key Concepts

- **Markdown-first ingestion**: MarkItDown uses Markdown as the canonical output because it keeps structural information while remaining lightweight and easy to process in chunking, indexing, and prompt pipelines.
- **Stream-based converter architecture**: Converters operate on binary file-like streams instead of file paths, which avoids temp files and makes the system easier to embed in services and in-memory workflows.
- **Converter dispatch by format**: The core library selects specialized converters based on stream metadata, content type, URI handling, and installed capabilities.
- **Optional feature groups**: Support for formats like PDF, DOCX, PPTX, XLSX, and audio transcription is gated by extras, keeping default installs smaller and more modular.
- **LLM-assisted enrichment**: Some workflows can use OpenAI-compatible models or Azure Document Intelligence for image descriptions, OCR, or transcription when conventional parsing is not enough.
- **Plugin extensibility**: Plugins are packaged separately and explicitly enabled, allowing third parties to add or override converters without modifying the core library.

## How It Works

MarkItDown is organized like a small monorepo with several packages:

- `packages/markitdown`: core library and CLI
- `packages/markitdown-ocr`: OCR-oriented plugin
- `packages/markitdown-sample-plugin`: reference plugin implementation
- `packages/markitdown-mcp`: MCP server wrapper

The central API is the `MarkItDown` class in `src/markitdown/_markitdown.py`, which powers both the CLI and Python usage. Supporting modules handle shared converter abstractions, stream metadata detection, URI normalization, and conversion-specific exceptions. Actual format logic lives in `src/markitdown/converters/`, with dedicated modules for PDFs, Office formats, HTML, images, audio, notebooks, archives, and more.

The processing flow is straightforward:

1. Input is provided as a path, URL, stdin, or stream.
2. The orchestration layer opens it as a binary stream and inspects metadata.
3. A matching converter is selected.
4. The converter extracts text and structure using format-specific tooling.
5. Output is normalized into Markdown and returned as a result object, typically accessed via `text_content`.

A few implementation choices are particularly useful for production systems. The library avoids temp files by default, expects binary streams for stream conversion, and activates some capabilities only when corresponding extras are installed. This keeps the base system lean while still supporting richer conversion stacks where needed.

The repository structure also reveals design intent. Office formats have dedicated handlers rather than generic fallback parsing, suggesting attention to preserving semantics like equations and formatting. PDF support appears mature, with tests aimed at tables, numbering, scanned reports, and memory-sensitive processing. ZIP archives are recursively unpacked and converted, which is helpful for bulk ingestion workflows. Media support relies on external tools such as `ffmpeg` and `exiftool`, reflecting a practical approach instead of forcing everything through pure Python.

LLM integration is optional and layered on top of deterministic conversion. In the core package, image captioning can be enabled with an OpenAI-compatible client. The OCR plugin extends this pattern by wrapping built-in converters and inserting OCR extraction for embedded or scanned content. This is an important architectural decision: the base package stays dependency-light and predictable, while plugins add heavier or AI-dependent behavior only when explicitly enabled.

The sample plugin is also worth studying because it shows the intended extension model for external developers. Combined with broad fixture-based tests across many real document types, the project serves not just as a useful tool but as a reference architecture for building heterogeneous document ingestion pipelines.

Operationally, the Dockerfile shows how the maintainers expect the system to run in containers: install core package extras, add plugin packages, include tools like `ffmpeg` and `exiftool`, and expose the CLI as the entrypoint. That makes it well suited for batch conversion jobs or service-side ingestion stages.

## Test Yourself

<details><summary>Why does MarkItDown use Markdown as its canonical output?</summary>

Markdown preserves useful document structure such as headings, lists, tables, and links while remaining lightweight. That makes it practical for chunking, indexing, retrieval, text analysis, and prompt pipelines.

</details>

<details><summary>How does MarkItDown keep its core installation lean while supporting many formats and AI-assisted features?</summary>

Format support is divided into optional dependency groups, while heavier or AI-dependent behavior can be supplied through explicitly enabled plugins. The lesson describes image captioning, OCR, and transcription as optional layers over deterministic conversion.

</details>

<details><summary>What is the main operational benefit of MarkItDown&#x27;s stream-based converter architecture?</summary>

Converters consume binary file-like streams rather than requiring file paths, so pipelines can process in-memory or service-provided content without creating temporary files. The orchestration layer inspects metadata, dispatches a specialized converter, and returns normalized Markdown through a result object such as `text_content`.

</details>

## Personal Notes

MarkItDown: Extensible File-to-Markdown Conversion for LLM Pipelines

Source: https://github.com/microsoft/markitdown
Notion page: https://www.notion.so/MarkItDown-Extensible-File-to-Markdown-Conversion-for-LLM-Pipelines-34501bb0839a81df8a09ee7716522c00

Tags: python, markdown, document-conversion, llm, plugins, pdf

Overview

MarkItDown is a Python-based conversion framework that turns many common document and media formats into structured Markdown. Its purpose is not pixel-perfect reproduction, but extraction of text and document structure in a form that is efficient for downstream use by LLMs, search, retrieval, and other text-analysis systems.

This repository is useful to engineers building ingestion pipelines for PDFs, Office files, HTML, notebooks, archives, images, and audio. Beyond the CLI, the codebase shows a practical architecture for stream-oriented conversion, optional dependency loading, plugin-based extension, and selective use of external AI services such as Azure Document Intelligence and OpenAI-compatible vision/transcription models.

Key Concepts

  *   Markdown-first ingestion: MarkItDown treats Markdown as the canonical output format because it preserves useful structure like headings, lists, tables, and links while remaining close to plain text. That makes it a good intermediate representation for LLM prompts, chunking pipelines, and indexing systems.
  *   Stream-based converter architecture: A notable design change in the project is that converters operate on binary file-like streams rather than file paths. This avoids temporary files, simplifies integration into services and pipelines, and makes conversion easier to compose with in-memory processing.
  *   Converter dispatch by format: The main package contains many specialized converters under `markitdown/converters`, each targeting a specific type such as PDF, DOCX, PPTX, XLSX, HTML, ZIP, audio, or images. The top-level orchestration layer determines which converter to use based on stream metadata, URI handling, and available dependencies.
  *   Optional feature groups: Support for some formats depends on optional dependencies declared in extras like `pdf`, `docx`, `pptx`, `xlsx`, or `audio-transcription`. This keeps the default install lighter while allowing production users to enable only the capabilities they need.
  *   LLM-assisted enrichment: Some converters can call an OpenAI-compatible client to generate image descriptions or perform OCR through plugins. This extends beyond pure parsing and enables extraction from image-heavy or scanned content when traditional text extraction is insufficient.
  *   Plugin extensibility: Plugins are packaged separately and disabled by default, then discovered and enabled explicitly. The repository includes both a sample plugin and a real OCR plugin, showing how third parties can override or augment built-in conversion behavior without modifying the core package.

How It Works

The repository is organized as a small monorepo with multiple Python packages:

- `packages/markitdown`: the core library and CLI - `packages/markitdown-ocr`: a plugin that adds OCR-aware converters - `packages/markitdown-sample-plugin`: a reference implementation for plugin authors - `packages/markitdown-mcp`: an MCP server wrapper for LLM application integration

At the center of the core package is `src/markitdown/_markitdown.py`, which exposes the main `MarkItDown` class used by both the Python API and CLI. The CLI entrypoint lives in `src/markitdown/__main__.py`. Supporting infrastructure includes:

- `_base_converter.py`: shared converter abstractions and result handling - `_stream_info.py`: stream metadata detection and normalization - `_uri_utils.py`: handling paths and URL-like inputs - `_exceptions.py`: conversion-specific errors

The actual format implementations are in `src/markitdown/converters/`. The file tree shows a deliberately modular design, with one converter per major type:

- `_pdf_converter.py` - `_docx_converter.py` - `_pptx_converter.py` - `_xlsx_converter.py` - `_html_converter.py` - `_image_converter.py` - `_audio_converter.py` - `_youtube_converter.py` - `_zip_converter.py` - `_ipynb_converter.py` - `_outlook_msg_converter.py` - `_epub_converter.py` - plus helpers like `_markdownify.py`, `_llm_caption.py`, and `_transcribe_audio.py`

The high-level data flow is:

1. A caller provides a file path, URL, stdin stream, or other input to the CLI or `MarkItDown.convert()`. 2. The orchestration layer opens the input as a binary stream and gathers enough metadata to infer content type and extension. 3. It selects a matching converter implementation. 4. The converter extracts text and structure, often using a format-specific library. 5. The output is normalized into Markdown and returned as a result object whose `text_content` can be printed, saved, or fed into another system.

A few implementation details matter for engineers integrating this library:

- **No temp files by default:** converters now consume file-like objects directly. - **Binary streams only:** `convert_stream()` expects bytes, not text streams. -
