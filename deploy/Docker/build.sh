rm -fr nerproject
mkdir -p nerproject/{data,tmp}
cp -r ../../doc ../../models ../../src nerproject
docker build -t nerproject:latest -f Dockerfile.nerproject .
