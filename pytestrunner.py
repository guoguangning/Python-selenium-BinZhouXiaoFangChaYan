import subprocess
from pathlib import Path
import time
from framework.logger import Logger


logger = Logger("pytest_run").get_log()


def run_pytest(allure_results_dir: Path):
    """
    运行 pytest 并生成 allure 结果。
    :param allure_results_dir: 存储 pytest allure 结果的目录
    """
    pattern = './testsuites/pytest/testLogin.py'
    try:
        logger.info("Running pytest...")
        result = subprocess.run([
            'pytest',
            pattern,
            f'--alluredir={allure_results_dir}'
        ], check=True, text=True, capture_output=True)

        logger.info(result.stdout)  # 记录 pytest 输出
        # logger.error(result.stderr)  # 记录 pytest 错误输出

    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while running pytest: {e}")
        logger.error(f"Return code: {e.returncode}")
        logger.error(f"Output: {e.output}")
        logger.error(f"Error output: {e.stderr}")
        raise  # 重新抛出异常以便外部方法可以捕获


def generate_allure_report(allure_results_dir: Path, html_report_dir: Path):
    """
    生成 Allure 报告。
    :param allure_results_dir: 存储 pytest allure 结果的目录
    :param html_report_dir: 生成的 HTML 报告目录
    """
    allure_cmd = 'C:\\allure-2.30.0\\bin\\allure.bat'

    try:
        logger.info("Generating Allure report...")
        command = [allure_cmd, 'generate', allure_results_dir, '-o', html_report_dir, '--clean']
        # 使用 subprocess.run 来执行 allure 生成命令
        result = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True
        )

        # # 记录 Allure 输出
        logger.info(result.stdout)  # 记录 Allure 输出
        # logger.error(result.stderr)  # 记录 Allure 错误输出

        logger.info(f"Allure report generated at: {html_report_dir}")

    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while generating Allure report: {e}")
        logger.error(f"Return code: {e.returncode}")
        logger.error(f"Output: {e.output}")
        logger.error(f"Error output: {e.stderr}")
        raise  # 重新抛出异常以便外部方法可以捕获


def generate_report():
    """
    生成测试报告的主方法，调用 run_pytest 和 generate_allure_report 方法。
    """
    # 获取当前时间，并定义报告的文件名和路径
    now = time.strftime("%Y%m%d%H%M", time.localtime())
    base_dir = Path(__file__).resolve().parent / 'test_report'
    allure_results_dir = base_dir / f'allure_results_{now}'
    html_report_dir = allure_results_dir / 'html_report'

    # 创建报告目录（如果不存在）
    base_dir.mkdir(parents=True, exist_ok=True)
    allure_results_dir.mkdir(parents=True, exist_ok=True)
    html_report_dir.mkdir(parents=True, exist_ok=True)

    try:
        run_pytest(allure_results_dir)
        generate_allure_report(allure_results_dir, html_report_dir)
        open_allure_report(html_report_dir)  # 打开报告
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


def open_allure_report(report_dir: Path):
    """
    打开生成的 Allure 报告。
    :param report_dir: 生成的 HTML 报告目录
    """
    allure_cmd = 'C:\\allure-2.30.0\\bin\\allure.bat'
    try:
        logger.info("Opening Allure report...")
        subprocess.run([allure_cmd, 'open', report_dir], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error opening Allure report: {e}")
        logger.error(f"Return code: {e.returncode}")
        logger.error(f"Output: {e.stdout}")
        logger.error(f"Error output: {e.stderr}")
        raise


if __name__ == "__main__":
    generate_report()

