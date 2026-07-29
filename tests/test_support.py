from __future__ import annotations

from tests.support import libraries_up_to


def test_library_counts_by_size():
    assert len(libraries_up_to(1)) == 11
    assert len(libraries_up_to(2)) == 77
    assert len(libraries_up_to(3)) == 363


def test_constants_scale_with_size():
    assert all(
        library.n_constants == 2 * len(library.ops)
        for library in libraries_up_to(2)
    )
