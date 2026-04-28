# AgriGPT Farmer Agent

A simple AI agent for farmers that provides crop advice, pest management tips, and weather-aware recommendations.

## Features

- CLI interaction for farmer questions
- OpenAI API integration with fallback local responses
- Structured error handling with step-by-step status output

## Setup

1. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

2. Set your OpenAI API key in environment variables:

```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

3. Run the agent:

```powershell
python agent.py
```

If `OPENAI_API_KEY` is not set, the agent will use local fallback advice.

## Example Usage

```text
> Ask AgriGPT for farming advice or type quit: What should I plant in a dry climate?
AgriGPT says: In dry climates, choose drought-tolerant crops such as millet, sorghum, chickpeas, or pearl millet. Use mulch, drip irrigation, and conserve soil moisture.
```
