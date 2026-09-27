from pathlib import Path

import pytest
import requests

from italian_champions_results import cli

DATA = Path(__file__).parent / "data"


def test_local_file_grouped_and_filtered(capsys):
    cli.main(["--file", str(DATA / "results.xml"), "--clubid", "0098"])
    out = capsys.readouterr().out
    assert out.startswith("Test Championship - 2026-09-12")
    assert "M ELITE" in out and "Rossi" in out and "Verdi" in out
    assert "Bianchi" not in out and "Neri" not in out


def test_winners_flag(capsys):
    cli.main(["--file", str(DATA / "results.xml"), "--clubid", "0098", "--winners"])
    out = capsys.readouterr().out
    assert "Rossi" in out and "Gialli" in out and "Rosa" in out
    assert "Verdi" not in out and "Grigi" not in out and "Hansen" not in out


def test_winners_without_results(capsys):
    cli.main(["--file", str(DATA / "results.xml"), "--clubid", "9999", "--winners"])
    assert "no winners for club 9999" in capsys.readouterr().out


def test_club_without_results(capsys):
    cli.main(["--file", str(DATA / "results.xml"), "--clubid", "9999"])
    assert "no results for club 9999" in capsys.readouterr().out


def test_download(monkeypatch, capsys):
    urls = []

    def fake_download(url, timeout=10):
        urls.append(url)
        return (DATA / "results.xml").read_bytes()

    monkeypatch.setattr(cli, "download_xml", fake_download)
    cli.main(["--id", "202613", "--clubid", "0982"])
    assert urls == ["https://www.fiso.it/_files/risultati_gara_files/imported/202613.xml"]
    assert "Neri" in capsys.readouterr().out


def test_network_error(monkeypatch, capsys):
    def fails(url, timeout=10):
        raise requests.ConnectionError("network down")

    monkeypatch.setattr(cli, "download_xml", fails)
    with pytest.raises(SystemExit) as e:
        cli.main(["--id", "1", "--clubid", "0098"])
    assert e.value.code == 1
    assert "Download error" in capsys.readouterr().err


def test_missing_file(capsys):
    with pytest.raises(SystemExit) as e:
        cli.main(["--file", "does_not_exist.xml", "--clubid", "0098"])
    assert e.value.code == 1
    assert "File not found" in capsys.readouterr().err


