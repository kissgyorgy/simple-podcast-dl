from podcast_dl import cli


convert = cli.EpisodeList().convert


def test_numeric_values():
    assert convert("1") == (["0001"], 0)
    assert convert("1,99") == (["0001", "0099"], 0)
    assert convert("0,9999") == (["0000", "9999"], 0)
    assert convert("0,9999,9999") == (["0000", "9999"], 0)


def test_ranges():
    assert convert("12-15") == (["0012", "0013", "0014", "0015"], 0)
    assert convert("0-3") == (["0000", "0001", "0002", "0003"], 0)
    assert convert("0-2,99-101") == (
        ["0000", "0001", "0002", "0099", "0100", "0101"],
        0,
    )
    assert convert("3-3") == (["0003"], 0)
    assert convert("3-3,3-3") == (["0003"], 0)


def test_last():
    assert convert("last") == ([], 1)
    assert convert("lAsT") == ([], 1)
    assert convert("last,last") == ([], 1)
    assert convert("last,last,last:5") == ([], 5)
    assert convert("last,last:10,last:5") == ([], 10)
    assert convert("last,last:10,last") == ([], 10)


def test_last_n():
    assert convert("last:5") == ([], 5)
    assert convert("last,last:5") == ([], 5)
    assert convert("last,last,last:5") == ([], 5)
    assert convert("last,lAst:10,laSt:5") == ([], 10)


def test_not_numeric_or_unknown():
    assert convert("the-changelog-afk-jeff-bonus.mp3") == (
        ["THE-CHANGELOG-AFK-JEFF-BONUS.MP3"],
        0,
    )

    assert convert("Some Title") == (["SOME TITLE"], 0)
    assert convert("1,") == (["0001"], 0)
    assert convert("3,10bla") == (["0003", "10BLA"], 0)
    assert convert("2-10bla") == (["2-10BLA"], 0)


def test_mixed_values():
    assert convert("1,99,12-14,last,the-changelog") == (
        ["0001", "0012", "0013", "0014", "0099", "THE-CHANGELOG"],
        1,
    )
    assert convert("0,12-14,last:5") == (["0000", "0012", "0013", "0014"], 5)


def test_EpisodeParam_ordering():
    assert cli.EpisodeParam("0005") < cli.EpisodeParam("0010")
    assert cli.EpisodeParam("0005") < cli.EpisodeParam("unknown")


def test_EpisodeParam_equality_with_strings():
    assert cli.EpisodeParam("0005") == "0005"
    assert cli.EpisodeParam("unknown") == "unknown"


def test_EpisodeParam_compare_is_case_insensitive():
    assert cli.EpisodeParam("CaMeLCaSeOrIdonteven") == "camelcaseoridonteven"
    assert cli.EpisodeParam("capitall") == "CAPITALL"
