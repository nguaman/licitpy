from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List

from tqdm import tqdm

from licitpy.entities.tender import Tender
from licitpy.settings import settings


def execute_concurrently(
    function: Callable[[Tender], bool],
    items: List[Tender],
    desc: str,
    max_workers: int = 8,
) -> List[Tender]:

    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(function, item): item for item in items}
        for future in tqdm(
            as_completed(futures),
            total=len(futures),
            desc=desc,
            disable=settings.disable_progress_bar,
        ):
            item = futures[future]
            try:
                if future.result():
                    results.append(item)
            except Exception as e:
                print(f"Error procesando {item}: {e}")

    return results
