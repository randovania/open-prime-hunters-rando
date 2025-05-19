from open_prime_hunters_rando.file_manager import FileManager


def patch_hints(file_manager: FileManager, hints: dict[str, str]) -> None:
    scan_log = file_manager.get_string_table("ScanLog")

    for hint in hints:
        string_id = hint["string_id"]
        string = hint["string"]

        string_entry = scan_log.get_string(string_id)
        string_entry.string = string
