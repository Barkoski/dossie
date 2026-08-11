# Identificacao documental e triagem

Aplicar quando a conversa contiver texto de autos, eventos, anexos ou paginas. O objetivo e criar um mapa verificavel do material recebido antes da analise probatoria.

## Sequencia

1. Percorrer o material na ordem em que aparece.
2. Detectar fronteiras por cabecalho, evento, titulo, assinatura, mudanca de emissor ou numeracao; nao separar apenas por mudanca de assunto.
3. Criar um documento por unidade autonoma. Se um evento contiver varias pecas, segmentar; se varias paginas formarem a mesma peca, manter juntas.
4. Registrar inicio e fim exatamente como expostos. Usar `?` quando ausentes e marcar a delimitacao `INCERTA` quando a fronteira nao estiver demonstrada.
5. Resumir o conteudo em uma ou duas frases concretas, sem conclusao juridica nova.
6. Somente depois ligar documento a fato, requisito ou tese.

## Familias documentais

Usar uma familia estavel e um tipo normalizado descritivo:

- `PECA_PROCESSUAL`: inicial, contestacao, replica, recurso, contrarrazoes, peticao.
- `DECISAO`: despacho, decisao interlocutoria, sentenca, acordao, voto.
- `ATO_PROCESSUAL`: citacao, intimacao, certidao, ata, mandado, termo.
- `PROVA_PESSOAL`: depoimento, declaracao, autodeclaracao, entrevista.
- `PROVA_MEDICA`: atestado, laudo, exame, prontuario, receituario.
- `PROVA_LABORAL_PREVIDENCIARIA`: CNIS, CTPS, PPP, LTCAT, GPS, carta de concessao, processo administrativo.
- `PROVA_CIVIL`: certidao civil, identidade, comprovante de residencia, procuracao.
- `PROVA_ECONOMICA`: nota fiscal, contrato, recibo, extrato, ficha financeira, calculo.
- `PROVA_RURAL`: bloco de produtor, cadastro rural, INCRA, ITR, declaracao sindical.
- `PARECER_OU_LAUDO`: parecer tecnico, pericia, relatorio especializado.
- `MIDIA`: fotografia, audio, video ou outro arquivo multimidia.
- `OUTRO`: usar somente quando nenhuma familia couber e explicar o tipo.

Nao copiar cegamente o rotulo cadastrado no sistema. Preservar esse rotulo em observacao quando divergir do conteudo e classificar pelo que o documento efetivamente e, marcando a confianca.

## Campos e confianca

Cada documento deve conter: `familia`, `tipo`, `evento_inicio`, `pagina_inicio`, `evento_fim`, `pagina_fim`, `resumo`, `criterio_delimitacao` e `confianca_identificacao`.

Confianca:

- `ALTA`: titulo, cabecalho ou metadado confirma tipo e limites.
- `MEDIA`: conteudo confirma o tipo, mas um limite depende da sequencia.
- `BAIXA`: fragmento, OCR ruim ou ausencia de marcadores impede identificacao segura.

Confianca baixa nao impede o registro; gera item em `confirmar`.

## Triagem

Preencher `triagem` apenas com o material do caso:

- `tipo_procedimento`: classe ou recurso identificado; `?` se ausente.
- `assunto_principal`: rotulo curto, sem antecipar a conclusao.
- `questao_central`: pergunta juridica enfrentada nos documentos.
- `pontos_controvertidos`: divergencias efetivamente presentes.
- `palavras_chave`: termos que descrevem fatos, beneficio e entidades; nao inserir nomes pessoais.
- `normas_invocadas`: somente normas ou precedentes citados no material, com origem rastreavel.
- `origem_conversa`: trecho, arquivo ou intervalo que sustenta a triagem.

Nao declarar conhecimento juridico atualizado, nao completar norma de memoria e nao converter classificacao documental em conclusao sobre o merito.
