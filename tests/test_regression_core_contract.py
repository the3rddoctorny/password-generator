def test_generate_always_produces_non_empty_password(page):
    # Contract test: generation must always produce a non-empty password.
    for _ in range(10):
        page.generate()
        assert page.password().strip()

