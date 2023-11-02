from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
import subprocess

class predictOperator(BaseOperator):
    """
    커스텀 데이터 업데이트 Operator
    """

    @apply_defaults
    def __init__(self, script_path, *args, **kwargs):
        """
        생성자

        :param script_path: 실행할 스크립트 파일의 경로
        :type script_path: str
        """
        super(predictOperator, self).__init__(*args, **kwargs)
        self.script_path = script_path

    def execute(self, context):
        """
        Operator 실행

        :param context: Airflow 작업 실행 컨텍스트 (사용되지 않음)
        :type context: dict
        """
        self.log.info("데이터 업데이트 스크립트를 실행합니다: %s", self.script_path)

        try:
            subprocess.run(['python', self.script_path], check=True)
            self.log.info("데이터 업데이트 스크립트 실행이 완료되었습니다.")
        except subprocess.CalledProcessError as e:
            self.log.error("데이터 업데이트 스크립트 실행 중 오류 발생: %s", e)
            raise e
