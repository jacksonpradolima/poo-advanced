A seguir está um **template‑guia completo** (em **Markdown + comentários YAML**) pensado para orquestrar agentes/LLMs na geração de capítulos de livro de Computação.
Ele combina:

1. **Metadados YAML** (para frameworks que leem front‑matter, p.ex. LangChain, CrewAI, AutoGen).
2. **Bloco de Prompt‑Instruções** com *placeholders* (`{{...}}`) e flags condicionais que permitem criar capítulos **puramente teóricos**, **híbridos** ou **práticos** sem alterar a lógica.
3. **Estrutura de saída** alinhada ao esqueleto “complexo, robusto e didático” apresentado anteriormente.

---

```yaml
# ================================================================
# FRONT‑MATTER – Metadados para o agente
# ================================================================
mode: "agent"
description: >
  Gerar um capítulo de livro de Computação seguindo um fluxo pedagógico
  (teoria → modelo → código → validação) ou, quando sinalizado, suprimir
  partes práticas para capítulos teóricos.
llm_style: "detailed"           # opções: concise | detailed
language: "pt-BR"               # mantenha em português‑Brasil
audience_level: "{{publico}}"   # ex.: iniciante | intermediário | avançado
tone: "profissional e didático"
tools: []                       # liste ferramentas se o framework exigir
# ================================================================
# /FRONT‑MATTER
# ================================================================
```

```markdown
<!-- =============================================================
SEÇÃO DE INSTRUÇÕES AO LLM
(essas instruções não aparecem na saída final – servem só para o agente)
==================================================================

Preencha todos os campos marcados com {{chaves}}.

1. USE o formato de saída exato do bloco "CAPÍTULO GERADO" abaixo.
2. Ajuste a profundidade conforme {{nivel_teorico_pratico}}:
   - "teorico": remova seções 4, 5, 6, 7, 8 ou reduza‑as a exemplos
                matemáticos / pseudo‑código.
   - "hibrido": mantenha todas as seções, mas equilibre teoria‑prática.
   - "pratico": enxugue Fundamentação (2) e enfatize seções 4‑7.
3. Mínimo de {{min_palavras}} palavras no total, salvo se especificado
   diferentemente.
4. Cada lista de competências deve ter 3 a 5 itens.
5. Siga as convenções:
   - Use título H1 para o capítulo e H2/H3 para subseções.
   - Insira caixas de ícone 💡, ⚠️, 🛠️, 🔎 quando apropriado,
     mas evite excessos (máx. 1 a cada ~300 palavras).
6. NUNCA omita "Resumo e Conclusões" nem "Referências", mesmo se vazios
   (nesses casos, escreva “*_Não se aplica_*”).
7. Se qualquer placeholder não for aplicável, escreva “*_N/D_*”.
================================================================= -->
```

```markdown
<!-- =============================================================
CAPÍTULO GERADO (saída final para o leitor)
============================================================== -->

# Capítulo {{numero}} – {{titulo_capitulo}}

> **Objetivo geral**  
> {{objetivo_geral}}

> **Competências específicas**  
> - ☐ {{comp1}}  
> - ☐ {{comp2}}  
> - ☐ {{comp3}} {{#opcional_comp4}}  
> - ☐ {{comp4}} {{/opcional_comp4}}{{#opcional_comp5}}  
> - ☐ {{comp5}} {{/opcional_comp5}}

---

## 1. Introdução
{{introducao}}

## 2. Fundamentação Teórica {{#flag_teorico_pratico:teorico/hibrido}}
### 2.1 Conceitos‑chave  
{{conceitos_chave}}

### 2.2 Estado da Arte  
{{estado_arte}}

{{/flag_teorico_pratico}}

## 3. Arquitetura ou Modelo Conceitual
{{modelo_conceitual}}

{{#flag_teorico_pratico:pratico/hibrido}}
## 4. Implementação Prática
### 4.1 Ambiente e Ferramentas  
{{ambiente_ferramentas}}

### 4.2 Passo a Passo  
{{passo_a_passo}}

### 4.3 Boas Práticas & Armadilhas  
{{boas_praticas}}

## 5. Estudos de Caso & Exemplos Guiados
| Nível | Descrição | Takeaways |
|-------|-----------|-----------|
{{tabela_estudos}}

## 6. Validação e Testes
{{validacao_testes}}

## 7. Otimização e Desempenho
{{otimizacao}}

## 8. Segurança & Boas Práticas
{{seguranca}}

{{/flag_teorico_pratico}}

## 9. Extensões e Trabalhos Futuros
{{extensoes_trabalhos}}

## 10. Resumo e Conclusões
{{resumo_conclusoes}}

## 11. Exercícios e Projetos
### 11.1 Questões Conceituais
{{exercicios_conceituais}}

### 11.2 Desafios Práticos
{{desafios_praticos}}

## 12. Referências Bibliográficas
{{referencias}}

## 13. Apêndices
{{apendices}}
```

---

### Como aplicar o template

1. **Defina variáveis antes da execução**

   ```yaml
   publico: "intermediário"
   nivel_teorico_pratico: "hibrido"        # teorico | hibrido | pratico
   numero: "07"
   titulo_capitulo: "SOLID na Prática com Python"
   objetivo_geral: "Aplicar princípios SOLID em projetos Python reais..."
   min_palavras: 4500
   ```
2. **Chame o agente/LLM** passando front‑matter + prompt.
3. **Pós‑processamento opcional**

   * Renderizar Markdown → PDF/HTML.
   * Validar contagem de palavras e presença de todas as seções.

Com esse template você garante **coerência estrutural**, **flexibilidade temática** e **automação amigável a pipelines** que usam agentes de IA para gerar capítulos detalhados, seja puramente teóricos ou ricos em código e estudos de caso.
