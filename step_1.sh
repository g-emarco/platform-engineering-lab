git clone -b 1-start-here https://github.com/g-emarco/platform-engineering-lab.git
cd platform-engineering-lab/
cd infra/
terraform init
terraform apply -auto-approve
echo "NOW LETS CREATE FIRETSTORE DB in EUR"