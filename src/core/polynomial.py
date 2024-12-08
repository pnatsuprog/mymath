from typing import Dict, Tuple, Union


class Polynomial:
    # _VariablePart: 単項式(多変数対応)の変数部を各変数の指数を表すタプルで定義
    # タプルのインデックスが対応する変数の添字となる
    # 例:  (x0^2)(x1^3)(x2^1) を表すには (2, 3, 1) とする
    _VariablePart = Tuple[int, ...]

    # Terms: ペア{キー:値}を1つの項（単項式）とし、ペアの総和を多項式と考える辞書型で多項式を定義
    # キー: ある項（単項式）の変数部を _VariablePart型 で表す
    # 値: 当該ペアが担う項の係数の値を float型 で表す
    # 例: 4(x0^2)(x1^3)(x2^1) + x2^2 を表すには {(2, 3, 1): 4, (0, 0, 2): 1} とする
    # 定数項を表したい場合は空のタプル () をキーとする
    _Terms = Dict[_VariablePart, float]

    terms: _Terms

    def __init__(self, terms: Union[_Terms, None] = None) -> None:
        """
        多変数の多項式を表現するクラス。

        :param terms: 多項式の各項を表す辞書
                        キー: 各変数の指数のタプル (例: (2, 1) -> x^2y)
                        値: 係数を表す float型 の値
                            ※定数項を表す場合は空のタプル () をキーとする
        """
        if terms is None:
            self.terms = {}
        elif not isinstance(terms, dict):
            raise ValueError("terms は 辞書型 である必要があります。")
        else:
            self.terms = {}  # 同類項があれば1つにまとめたいので、直接 terms をセットせずに add_term() を使う
            for var_part, coefficient in terms.items():
                self.add_term(coefficient, var_part)

    def __repr__(self) -> str:
        if not self.terms:
            return "Polynomial(0)"
        terms_str = " + ".join(
            f"{coefficient}"
            + (
                ""
                if var_part == ()
                else f"*{'*'.join([f'x{i}^{exponent}' for i, exponent in enumerate(var_part) if exponent > 0])}"
            )
            for var_part, coefficient in sorted(
                self.terms.items(), key=lambda item: item[0], reverse=True
            )
        )
        return f"Polynomial({terms_str})"

    def _validate_variable_part(self, var_part: _VariablePart) -> None:
        """
        変数部が非負整数のタプルで構成されているか検証する。

        :param var_part: 検証する変数部
        :raises ValueError: 非負整数で構成されていない場合
        """
        if not isinstance(var_part, tuple):
            raise ValueError(f"変数部 {var_part} はタプル型である必要があります。")
        if not all(isinstance(exp, int) and exp >= 0 for exp in var_part):
            raise ValueError(
                f"変数部 {var_part} には非負整数のみが含まれている必要があります。"
            )

    def add_term(self, coefficient: float, var_part: _VariablePart) -> None:
        """
        新しい単項式を多項式に追加する。
        （同類項があれば1つにまとめます。）

        :param var_part: 追加する単項式の変数部
        :param coefficient: 追加する単項式の係数
        """
        self._validate_variable_part(var_part)

        # 定数項のキーを統一
        if all(exp == 0 for exp in var_part):
            var_part = ()

        if var_part in self.terms:
            # 同類項が既に存在する場合は係数を加算するだけ
            self.terms[var_part] += coefficient

            # 係数が0になった場合は項を削除
            if self.terms[var_part] == 0:
                del self.terms[var_part]
        else:
            # 同類項が存在しない場合は新たに追加
            self.terms[var_part] = coefficient

    def __add__(self, other: "Polynomial") -> "Polynomial":
        """
        Polynomial 同士の足し算を定義します。

        :param other: 足し合わせる別の Polynomial インスタンス
        :return: 結果の Polynomial インスタンス
        """
        if not isinstance(other, Polynomial):
            raise TypeError("足し算の対象は Polynomial クラスである必要があります。")

        # 新しい辞書で足し算を実装
        result_terms = self.terms.copy()

        for var_part, coeff in other.terms.items():
            if var_part in result_terms:
                result_terms[var_part] += coeff

                # 係数が 0 になった場合は項を削除
                if result_terms[var_part] == 0:
                    del result_terms[var_part]
            else:
                result_terms[var_part] = coeff

        return Polynomial(result_terms)
