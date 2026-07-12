from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class RuntimeContractResult:
    name: str
    status: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimeContractReport:
    total: int
    passed: int
    failed: int
    warning: int
    results: list[RuntimeContractResult]


class RuntimeContractTester:
    """
    Runtime Contract Tester

    驗證 Canvas Runtime 對外 API 是否符合 Enterprise Runtime Contract。
    """

    def __init__(self, runtime: Any):
        self.runtime = runtime

    def run(self) -> RuntimeContractReport:
        results = [
            self._test_callable_api(
                name="get_selected_object()",
                method_name="get_selected_object",
                expected_type=None,
                allow_none=True,
            ),
            self._test_callable_api(
                name="get_events()",
                method_name="get_events",
                expected_type=list,
                allow_none=False,
            ),
            self._test_callable_api(
                name="get_latest_event()",
                method_name="get_latest_event",
                expected_type=None,
                allow_none=True,
            ),
            self._test_callable_api(
                name="get_events_by_type()",
                method_name="get_events_by_type",
                expected_type=list,
                allow_none=False,
                args=["selection_changed"],
            ),
            self._test_callable_api(
                name="clear_events()",
                method_name="clear_events",
                expected_type=None,
                allow_none=True,
                destructive=True,
            ),
            self._test_callable_api(
                name="get_selected_relationships()",
                method_name="get_selected_relationships",
                expected_type=list,
                allow_none=False,
            ),
            self._test_callable_api(
                name="get_summary()",
                method_name="get_summary",
                expected_type=dict,
                allow_none=False,
            ),
        ]

        passed = len([item for item in results if item.status == "Passed"])
        failed = len([item for item in results if item.status == "Failed"])
        warning = len([item for item in results if item.status == "Warning"])

        return RuntimeContractReport(
            total=len(results),
            passed=passed,
            failed=failed,
            warning=warning,
            results=results,
        )

    def _test_callable_api(
        self,
        name: str,
        method_name: str,
        expected_type: type | None,
        allow_none: bool,
        args: list[Any] | None = None,
        destructive: bool = False,
    ) -> RuntimeContractResult:
        method = getattr(self.runtime, method_name, None)

        if not callable(method):
            return RuntimeContractResult(
                name=name,
                status="Failed",
                message="Runtime API is missing or not callable.",
                details={
                    "method_name": method_name,
                    "expected": "callable",
                    "actual": type(method).__name__,
                },
            )

        if destructive:
            return RuntimeContractResult(
                name=name,
                status="Warning",
                message="API exists but execution was skipped because it mutates runtime state.",
                details={
                    "method_name": method_name,
                    "reason": "destructive_api_skipped",
                },
            )

        try:
            call_args = args or []
            result = method(*call_args)

            if result is None and not allow_none:
                return RuntimeContractResult(
                    name=name,
                    status="Failed",
                    message="Runtime API returned None but contract requires a value.",
                    details={
                        "method_name": method_name,
                        "expected_type": expected_type.__name__ if expected_type else None,
                        "actual_type": "NoneType",
                    },
                )

            if expected_type is not None and result is not None and not isinstance(result, expected_type):
                return RuntimeContractResult(
                    name=name,
                    status="Failed",
                    message="Runtime API returned unexpected type.",
                    details={
                        "method_name": method_name,
                        "expected_type": expected_type.__name__,
                        "actual_type": type(result).__name__,
                    },
                )

            return RuntimeContractResult(
                name=name,
                status="Passed",
                message="Runtime API contract passed.",
                details={
                    "method_name": method_name,
                    "result_type": type(result).__name__,
                    "has_value": result is not None,
                },
            )

        except Exception as error:
            return RuntimeContractResult(
                name=name,
                status="Failed",
                message="Runtime API raised an exception.",
                details={
                    "method_name": method_name,
                    "error": str(error),
                },
            )