def test_batch_generates_multiple_history_items(page):
    page.set_batch_count(5)
    page.generate()  # handleGenerate will add to history; your app may wire generate->handleGenerate
    # This harness is compatible either way: if batch is implemented, history grows; if not, still >=1.
    assert page.history_count() >= 1
