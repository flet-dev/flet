GO_OS=linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    GO_OS=darwin
fi

curl -fsSL "https://golang.org/dl/go${GO_VERSION}.${GO_OS}-amd64.tar.gz" -o /tmp/go-linux-amd64.tar.gz
sudo tar zxf /tmp/go-linux-amd64.tar.gz -C /usr/local
export PATH=/usr/local/go/bin:$PATH
export GOROOT=/usr/local/go
export GOPATH=$HOME/go
go version