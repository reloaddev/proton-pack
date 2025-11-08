import os
import pytest

from proton_pack.action import run


def test_run_success(tmp_path):
    # given
    input_file = tmp_path / "migration.txt"
    input_file.write_text("CREATE TABLE ghosts;")
    os.environ["MIGRATION_FILE"] = str(input_file)

    output_file = tmp_path / "output.txt"
    output_file.write_text("")
    os.environ["GITHUB_OUTPUT"] = str(output_file)

    # when
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()

    # then
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_run_invalid_result(tmp_path):
    # given
    input_file = tmp_path / "dangerous_migration.txt"
    input_file.write_text("""
        CREATE TABLE ghost (id INTEGER PRIMARY KEY, name TEXT, type TEXT, reporter_id INTEGER);
        ALTER TABLE ghost ADD CONSTRAINT fk_reporter FOREIGN KEY (reporter_id) REFERENCES human(id);
    """)
    os.environ["MIGRATION_FILE"] = str(input_file)

    output_file = tmp_path / "output.txt"
    output_file.write_text("")
    os.environ["GITHUB_OUTPUT"] = str(output_file)

    # when
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()

    # then
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_run_file_not_found():
    # given
    os.environ["MIGRATION_FILE"] = "non-existing-file.txt"

    # when + then
    with pytest.raises(FileNotFoundError) as pytest_wrapped_e:
        run()

    # then
    assert pytest_wrapped_e.type == FileNotFoundError