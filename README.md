Descrição do Projeto
Este projeto implementa uma arquitetura serverless na AWS para processamento automático de notas fiscais. Quando um arquivo JSON com notas fiscais é enviado para um bucket S3, uma função Lambda é automaticamente acionada para processar os dados e armazená-los em uma tabela DynamoDB.

Arquivo JSON → Amazon S3 → AWS Lambda → Amazon DynamoDB

Awquivos Utilizados:
├── grava_db.py # Código Lambda principal
├── lambda_function.zip # Pacote de implantação
├── notification.json # Configuração do trigger S3
├── notas_fiscais.json # Dados de exemplo para testes

Criação do Bucket S3
# Criar bucket para upload de notas fiscais
awslocal s3api create-bucket --bucket notas-fiscais-upload

# Verificar bucket criado
awslocal s3api list-buckets

Criação da Tabela DynamoDB
aws dynamodb create-table --table-name NotasFiscais --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --billing-mode PAY_PER_REQUEST --endpoint-url http://localhost:4566

Função Lambda Principal
Arquivo grava_db.py

Implantação da Função Lambda
Criar pacote:
powershell "Compress-Archive -Path grava_db.py -DestinationPath lambda_function.zip"

Criar função Lambda:
aws --endpoint-url=http://localhost:4566 lambda create-function --function-name ProcessarNotasFiscais --runtime python3.9 --role arn:aws:iam::000000000000:role/lambda-role --handler grava_db.lambda_handler --zip-file fileb://lambda_function.zip

Configuração de Permissões
Criar role IAM:
aws iam create-role --role-name lambda-role --assume-role-policy-document "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"lambda.amazonaws.com\"},\"Action\":\"sts:AssumeRole\"}]}" --endpoint-url=http://localhost:4566

Permitir S3 invocar Lambda:
aws lambda add-permission --function-name ProcessarNotasFiscais --statement-id s3-trigger --action lambda:InvokeFunction --principal s3.amazonaws.com --source-arn arn:aws:s3:::notas-fiscais-upload --endpoint-url=http://localhost:4566


 Configuração do Trigger S3
 Arquivo notification.json
 
Aplicar configuração:
aws s3api put-bucket-notification-configuration --bucket notas-fiscais-upload --notification-configuration file://notification.json --endpoint-url=http://localhost:4566

 Testes
Dados de exemplo (notas_fiscais.json)

Comandos de teste:

# Upload do arquivo
aws s3 cp notas_fiscais.json s3://notas-fiscais-upload/ --endpoint-url=http://localhost:4566

# Verificar logs
aws logs describe-log-streams --log-group-name /aws/lambda/ProcessarNotasFiscais --endpoint-url=http://localhost:4566

# Consultar dados
aws dynamodb scan --table-name NotasFiscais --endpoint-url=http://localhost:4566

Funcionalidades
Processamento automático de arquivos JSON
Validação de dados de notas fiscais
Armazenamento em DynamoDB
Organização automática de arquivos
Logs detalhados para monitoramento
Filtro por tipo de arquivo (.json)

Resultados
Redução de processamento manual
Maior confiabilidade nos dados
Escalabilidade automática
Custo otimizado (pay-per-use)

Próximas Melhorias
API Gateway para consultas
Mais validações de dados
Dashboard de visualização
Integração com serviços de notificação



