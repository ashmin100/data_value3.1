"""데이터가치 에이전트 - 메인 실행 파일"""

import argparse
import sys
from typing import Optional

from src.agent.main_agent import run_agent
from src.presets.modes import (
    run_quick_scan,
    run_default_report,
    run_timeseries_analysis,
    run_value_assessment,
    run_qualitative_evaluation
)


def main():
    parser = argparse.ArgumentParser(
        description="데이터가치 에이전트 - CSV 자동 분석 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  # 에이전트 모드 (자연어 쿼리)
  python main.py --csv data.csv --query "데이터 품질을 빠르게 확인하고 싶어요"
  python main.py --csv data.csv --query "시계열 데이터인지 확인하고 가치평가해줘"
  
  # 직접 모드 지정
  python main.py --csv data.csv --mode quick_scan
  python main.py --csv data.csv --mode default_report
  python main.py --csv data.csv --mode timeseries_analysis
  python main.py --csv data.csv --mode value_assessment --target price
  python main.py --mode qualitative_evaluation --meta-file meta.json
  
  # LLM 프로바이더 변경
  python main.py --csv data.csv --query "분석해줘" --provider anthropic
        """
    )
    
    # 필수 인자 (csv는 qualitative_evaluation 모드에서는 선택적일 수 있음, 하지만 argparse 구조상 required=True면 곤란)
    # 구조 변경: --csv를 optional로 바꾸고, 모드에 따라 체크
    parser.add_argument(
        "--csv",
        required=False,
        help="./breast_cancer_dataset.csv" # 경로 변경 가능
    )
    
    # 실행 방식
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--query",
        help="데이터 품질을 빠르게 확인하고 싶어요" # 프롬프트 변경 가능
    )
    group.add_argument(
        "--mode",
        choices=["quick_scan", "default_report", "timeseries_analysis", "value_assessment", "qualitative_evaluation"],
        help="value_assessment"
    )
    
    # 옵션 파라미터
    parser.add_argument(
        "--target",
        help="타겟 변수 (value_assessment 모드에서 사용)"
    )
    parser.add_argument(
        "--time-col",
        help="시간 컬럼명 (timeseries_analysis 모드에서 사용)"
    )
    parser.add_argument(
        "--ref-data",
        help="시장 가치 평가용 참조 데이터 경로 (value_assessment 모드에서 사용)"
    )
    parser.add_argument(
        "--meta-file",
        help="정성적 가치 평가용 메타데이터 JSON 파일 경로 (qualitative_evaluation 모드에서 필수)"
    )
    
    # LLM 설정
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic", "gemini"],
        help="gemini"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=True,
        help="상세 로그 출력 (기본값: True)"
    )
    
    args = parser.parse_args()
    
    # 입력 검증
    import os
    
    # qualitative_evaluation 모드가 아닐 때는 csv 필수
    if args.mode != "qualitative_evaluation" and not args.query:
        if not args.csv:
            parser.error("--csv argument is required unless mode is 'qualitative_evaluation' or using --query")
            
    if args.csv and not os.path.exists(args.csv):
        print(f"❌ 오류: CSV 파일을 찾을 수 없습니다: {args.csv}")
        sys.exit(1)
    
    # Windows 콘솔 인코딩 설정
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("📊 데이터가치 에이전트")
    print("=" * 60)
    if args.csv:
        print(f"📂 CSV 파일: {args.csv}")
    
    try:
        # 에이전트 모드
        if args.query:
            if not args.csv:
                 print("❌ 오류: 에이전트 모드(--query)를 사용하려면 --csv가 필요합니다.")
                 sys.exit(1)

            print(f"💬 사용자 쿼리: {args.query}")
            print(f"🤖 LLM 프로바이더: {args.provider or '환경변수 기본값'}")
            print()
            
            result = run_agent(
                csv_path=args.csv,
                query=args.query,
                llm_provider=args.provider,
                verbose=args.verbose
            )
            
            if result["success"]:
                print("\n" + "=" * 60)
                print("✅ 분석 완료!")
                print("=" * 60)
                print(result["output"])
            else:
                print(f"\n❌ 오류 발생: {result['error']}")
                sys.exit(1)
        
        # 직접 모드 실행
        elif args.mode:
            print(f"⚙️ 실행 모드: {args.mode}")
            print()
            
            if args.mode == "quick_scan":
                result = run_quick_scan.invoke({"csv_path": args.csv})
            
            elif args.mode == "default_report":
                result = run_default_report.invoke({"csv_path": args.csv})
            
            elif args.mode == "timeseries_analysis":
                result = run_timeseries_analysis.invoke({
                    "csv_path": args.csv,
                    "time_col": args.time_col
                })
            
            elif args.mode == "value_assessment":
                result = run_value_assessment.invoke({
                    "csv_path": args.csv,
                    "target": args.target,
                    "ref_data": args.ref_data
                })
                
            elif args.mode == "qualitative_evaluation":
                if not args.meta_file:
                    print("❌ 오류: qualitative_evaluation 모드에서는 --meta-file이 필요합니다.")
                    sys.exit(1)
                    
                result = run_qualitative_evaluation.invoke({
                    "meta_path": args.meta_file,
                    "csv_path": args.csv # 선택적
                })
            
            # print("\n" + "=" * 60)
            # print("✅ 분석 완료!")
            # print("=" * 60)
            
        
        # 아무것도 지정 안 한 경우: 기본 리포트
        else:
            print("⚙️ 실행 모드: default_report (기본값)")
            print()
            
            result = run_default_report.invoke({"csv_path": args.csv})
            
            # print("\n" + "=" * 60)
            # print("✅ 분석 완료!")
            # print("=" * 60)
            
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자에 의해 중단되었습니다.")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ 예기치 않은 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

