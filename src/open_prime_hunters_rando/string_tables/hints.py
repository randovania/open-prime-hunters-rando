from open_prime_hunters_rando.file_manager import FileManager, Language


def patch_hints(file_manager: FileManager, hints: dict[str, str]) -> None:
    scan_log = file_manager.get_string_table(Language.ENGLISH, "ScanLog")  # TODO: Change other languages

    for string_id, text in hints.items():
        string_entry = scan_log.get_string(string_id)
        string_entry.text = text
