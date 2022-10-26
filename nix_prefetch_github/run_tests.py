#!/usr/bin/env python

from __future__ import annotations

import argparse
import functools
import os
import sys
import time
import traceback
import types
import typing
import unittest
from dataclasses import dataclass, field

singleton = functools.lru_cache

Error = typing.Union[
    typing.Tuple[typing.Type[BaseException], BaseException, types.TracebackType],
    typing.Tuple[None, None, None],
]


class DependencyInjector:
    @singleton
    def get_configuration(self) -> Configuration:
        return Configuration()

    def get_controller(self) -> Controller:
        return Controller(configuration=self.get_configuration())

    def get_test_coordinator(self) -> TestCoordinator:
        return TestCoordinator(
            test_collector=self.get_test_collector(),
            report_generator=self.get_report_generator(),
            runner=self.get_test_runner(),
            display=self.get_display(),
        )

    def get_test_collector(self) -> TestCollector:
        return TestCollector(configuration=self.get_configuration())

    def get_report_generator(self) -> ReportGeneratorImpl:
        return ReportGeneratorImpl(timer=self.get_test_run_timer())

    def get_test_runner(self) -> TestRunner:
        return TestRunnerImpl(
            results=self.get_result_factory().construct_result(),
        )

    def get_result_factory(self) -> ResultFactory:
        return ResultFactory(
            display=self.get_display(),
            result_formatter=self.get_result_formatter(),
            timer=self.get_test_run_timer(),
            configuration=self.get_configuration(),
        )

    @singleton
    def get_display(self) -> Display:
        return Display()

    @singleton
    def get_test_run_timer(self) -> TestRunTimerImpl:
        return TestRunTimerImpl()

    def get_result_formatter(self) -> ResultFormatterImpl:
        return ResultFormatterImpl()


def ansi(*code: int) -> str:
    return f"\033[{';'.join(map(str, code))}m"


RED = ansi(1, 31)
WHITE = ansi(0)


class TestRunner(typing.Protocol):
    def run_test(self, test: unittest.TestCase) -> None:
        ...

    def get_results(self) -> unittest.TestResult:
        ...


class TestRunnerImpl:
    def __init__(self, results: unittest.TestResult):
        self.results = results

    def run_test(self, test: unittest.TestCase) -> None:
        test.run(self.results)

    def get_results(self) -> unittest.TestResult:
        return self.results


class Display:
    def __init__(self) -> None:
        self.last_flush = time.monotonic()

    def print(self, text: str) -> None:
        print(text, end="")
        if (current := time.monotonic()) - self.last_flush > 0.01:
            sys.stdout.flush()
            self.last_flush = current


@dataclass
class ResultFactory:
    display: Display
    result_formatter: ResultFormatter
    configuration: Configuration
    timer: TestRunTimer

    def construct_result(self) -> unittest.TestResult:
        return CustomTestResult(
            error_display=self.display,
            result_formatter=self.result_formatter,
            timer=self.timer,
            configuration=self.configuration,
        )


@dataclass
class TestCollector:
    configuration: Configuration

    def collect_tests(self) -> typing.Iterable[unittest.TestCase]:
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir=".")
        remaining_suites = [iter(suite)]
        while remaining_suites:
            current_suite = remaining_suites.pop()
            try:
                for candidate in current_suite:
                    if isinstance(candidate, unittest.TestSuite):
                        remaining_suites.append(current_suite)
                        remaining_suites.append(iter(candidate))
                        break
                    elif isinstance(
                        candidate, unittest.TestCase
                    ) and self._is_pattern_match(candidate):
                        yield candidate
            except StopIteration:
                pass

    def _is_pattern_match(self, test: unittest.TestCase) -> bool:
        if not self.configuration.test_patterns:
            return True
        return any(pattern in test.id() for pattern in self.configuration.test_patterns)


@dataclass
class TestCoordinator:
    test_collector: TestCollector
    report_generator: ReportGenerator
    runner: TestRunner
    display: Display

    def run_tests(self) -> None:
        for test in self.test_collector.collect_tests():
            self.runner.run_test(test)
        self.display.print("\n")
        results = self.runner.get_results()
        report = self.report_generator.generate_report(results)
        report.display_results(self.display)
        self.display.print("\n")
        if not report.is_success():
            sys.exit(1)


class ResultFormatter(typing.Protocol):
    def format_success(self, test: unittest.TestCase) -> str:
        ...

    def format_failure(self, test: unittest.TestCase, err: Error) -> str:
        ...

    def format_error(self, test: unittest.TestCase, err: Error) -> str:
        ...

    def format_skip(self, test: unittest.TestCase, reason: str) -> str:
        ...

    def format_expected_failure(self, test: unittest.TestCase, err: Error) -> str:
        ...

    def format_unexpected_success(self, test: unittest.TestCase) -> str:
        ...


class TestRunTimerImpl:
    def __init__(self) -> None:
        self._start_times: dict[str, int] = dict()
        self._stop_times: dict[str, int] = dict()

    def start_test(self, id: str) -> None:
        self._start_times[id] = time.monotonic_ns()

    def stop_test(self, id: str) -> None:
        self._stop_times[id] = time.monotonic_ns()

    def get_test_timing(self, id: str) -> typing.Optional[int]:
        if id not in self._start_times:
            return None
        if id not in self._stop_times:
            return None
        return self._stop_times[id] - self._start_times[id]

    def timed_tests(self) -> typing.Iterable[str]:
        for test_id in self._start_times.keys():
            if test_id in self._stop_times:
                yield test_id


class ResultFormatterImpl:
    def format_success(self, test: unittest.TestCase) -> str:
        return "."

    def format_failure(self, test: unittest.TestCase, err: Error) -> str:
        return f"{RED}F{WHITE}\n" + f"{test} failed\n" + self._format_errors(err)

    def format_error(self, test: unittest.TestCase, err: Error) -> str:
        return (
            f"{RED}E{WHITE}\n" + f"{test} raise an error\n" + self._format_errors(err)
        )

    def format_skip(self, test: unittest.TestCase, reason: str) -> str:
        return "s"

    def format_expected_failure(self, test: unittest.TestCase, err: Error) -> str:
        return "."

    def format_unexpected_success(self, test: unittest.TestCase) -> str:
        return f"{RED}F{WHITE}"

    def _format_errors(self, err: Error) -> str:
        traceback_exception = traceback.TracebackException(*err)
        return "".join(traceback_exception.format())


class ReportGenerator(typing.Protocol):
    def generate_report(self, results: unittest.TestResult) -> Report:
        ...


class Report(typing.Protocol):
    def is_success(self) -> bool:
        ...

    def display_results(self, display: Display) -> None:
        ...


@dataclass
class ReportGeneratorImpl:
    timer: TestRunTimer

    def generate_report(self, results: unittest.TestResult) -> Report:
        return ReportImpl(result=results, timer=self.timer)


@dataclass
class ReportImpl:
    result: unittest.TestResult
    timer: TestRunTimer

    def is_success(self) -> bool:
        return self.result.wasSuccessful()

    def display_results(self, display: Display) -> None:
        display.print("report:")
        if self.result.failures:
            display.print(f" failure: {len(self.result.failures)}")
        if self.result.errors:
            display.print(f" errors: {len(self.result.errors)}")
        if self.result.unexpectedSuccesses:
            display.print(
                f" unexpected successes: {len(self.result.unexpectedSuccesses)}"
            )
        if self.result.skipped:
            display.print(f" skipped: {len(self.result.skipped)}")
        display.print("\n")


class TestRunTimer(typing.Protocol):
    def start_test(self, id: str) -> None:
        ...

    def stop_test(self, id: str) -> None:
        ...

    def get_test_timing(self, id: str) -> typing.Optional[int]:
        ...

    def timed_tests(self) -> typing.Iterable[str]:
        ...


class CustomTestResult(unittest.TestResult):
    def __init__(
        self,
        *args: typing.Any,
        error_display: Display,
        result_formatter: ResultFormatter,
        timer: TestRunTimer,
        configuration: Configuration,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._display = error_display
        self._formatter = result_formatter
        self._timer = timer
        self._configuration = configuration

    def startTest(self, test: unittest.TestCase) -> None:
        super().startTest(test)
        if self._configuration.is_verbose:
            self._display.print(f"\n{test.id()} ")
        self._timer.start_test(test.id())

    def stopTest(self, test: unittest.TestCase) -> None:
        self._timer.stop_test(test.id())
        super().startTest(test)

    def addSuccess(self, test: unittest.TestCase) -> None:
        super().addSuccess(test)
        self._display.print(self._formatter.format_success(test))

    def addError(self, test: unittest.TestCase, err: Error) -> None:
        super().addError(test, err)
        self._display.print(self._formatter.format_error(test, err))

    def addFailure(self, test: unittest.TestCase, err: Error) -> None:
        super().addFailure(test, err)
        self._display.print(self._formatter.format_failure(test, err))

    def addSkip(self, test: unittest.TestCase, reason: str) -> None:
        super().addSkip(test, reason)
        self._display.print(self._formatter.format_skip(test, reason))

    def addExpectedFailure(self, test: unittest.TestCase, err: Error) -> None:
        super().addExpectedFailure(test, err)
        self._display.print(self._formatter.format_expected_failure(test, err))

    def addUnexpectedSuccess(self, test: unittest.TestCase) -> None:
        super().addUnexpectedSuccess(test)
        self._display.print(self._formatter.format_unexpected_success(test))


@dataclass
class Configuration:
    test_patterns: list[str] = field(default_factory=list)
    is_verbose: bool = False


@dataclass
class Controller:
    configuration: Configuration

    def parse_arguments(
        self, arguments: list[str], environment_variables: dict[str, str]
    ) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "pattern",
            nargs="*",
            help="Tests that don't contain one of the specified patterns are ignored. Default: All possible tests are executed.",
        )
        parser.add_argument("--verbose", "-v", action="store_true", default=False)
        parsed_args = parser.parse_args(arguments)
        self.configuration.test_patterns = parsed_args.pattern
        self.configuration.is_verbose = parsed_args.verbose


if __name__ == "__main__":
    injector = DependencyInjector()
    controller = injector.get_controller()
    coordinator = injector.get_test_coordinator()

    controller.parse_arguments(sys.argv[1:], dict(os.environ))
    coordinator.run_tests()
