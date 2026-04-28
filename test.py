# Test script for AgriGPT
from farmer_agent import PESTS_KNOWLEDGE_BASE, SCHEMES_KNOWLEDGE_BASE, FarmerAgent

# Test pest knowledge
rice_pests = PESTS_KNOWLEDGE_BASE['rice']['pests']
print(f'Rice pests loaded: {len(rice_pests)} entries')

# Test scheme knowledge
schemes = SCHEMES_KNOWLEDGE_BASE
print(f'Government schemes loaded: {len(schemes)} entries')

# Test agent creation without AI
agent = FarmerAgent('dummy_key')
print(f'Agent created successfully. AI available: {agent.use_ai}')

# Test pest search
result = agent._search_pests_knowledge('What pests affect rice?')
print(f'Pest search result: {result["pest"]}')

# Test scheme search
result = agent._search_schemes_knowledge('What is PM-KISAN?')
print(f'Scheme search result: {result["scheme"]}')

# Test chat functionality
response = agent.chat('What pests affect rice crops?', 'test123', '9876543210')
print(f'Chat response: {response["response"]}')
print(f'Sources: {response["sources"]}')

print('All tests passed!')