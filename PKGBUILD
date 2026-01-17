# Maintainer: Jeff Sebring <jeff@example.com>
pkgname=localmind
pkgver=0.1.0
pkgrel=1
pkgdesc="Local-first AI prompt runner for files and directories, with extensible AI model support"
arch=('x86_64')
url="https://github.com/jeffsebring/localmind"
license=('MIT')
depends=('python>=3.11' 'python-pip' 'ollama')
makedepends=('python-setuptools' 'python-wheel' 'python-build')
source=("https://github.com/jeffsebring/localmind/archive/refs/tags/v${pkgver}.tar.gz")
sha256sums=('SKIP')  # replace with actual SHA256 for production

build() {
    cd "${srcdir}/localmind-${pkgver}"
    # Build the package using PEP 517
    python -m build --wheel --no-isolation
}

package() {
    cd "${srcdir}/localmind-${pkgver}"
    
    # Install Python wheel into package directory
    python -m pip install --root="${pkgdir}" --no-deps --ignore-installed dist/localmind-*.whl
    
    # Symlink CLI for system-wide usage
    install -Dm755 "${pkgdir}/usr/lib/python*/site-packages/localmind/__main__.py" "${pkgdir}/usr/bin/lcm"
}
