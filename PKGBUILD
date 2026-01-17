pkgname=localmind
pkgver=0.1.0
pkgrel=1
pkgdesc="Local-first AI prompt runner for files and directories"
arch=('any')
url="https://github.com/jeffsebring/localmind"
license=('MIT')
depends=('python' 'ollama')
makedepends=('python-build' 'python-installer' 'python-setuptools' 'python-wheel')
source=("$pkgname-$pkgver.tar.gz::https://github.com/jeffsebring/localmind/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
  cd "$pkgname-$pkgver"
  python -m build --wheel --no-isolation
}

package() {
  cd "$pkgname-$pkgver"
  python -m installer --destdir="$pkgdir" dist/*.whl
}

