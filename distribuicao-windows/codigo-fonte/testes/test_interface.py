"""Regressões da apresentação do relatório e de erros na inicialização."""
import tempfile
import tkinter as tk
import unittest
from unittest.mock import patch

import acessos
import armazenamento
import interface
import usuarios


class TesteInterface(unittest.TestCase):
    def test_indicadores_exibidos_e_rolagem(self):
        with tempfile.TemporaryDirectory() as pasta:
            estado = armazenamento.vazio()
            pessoa = usuarios.cadastrar(estado, "900100", "Pessoa Exemplo", "estudante",
                                        "07:00", "18:00", "")
            acessos.registrar(estado, pessoa, "2026-11-18 10:00", "MAQ-A", "falha", [])
            armazenamento.salvar(pasta, estado, "REGISTRO_ACESSO", "900100")
            root = tk.Tk()
            root.withdraw()
            try:
                with patch.object(interface, "PASTA", pasta):
                    app = interface.SentinelaLogApp(root)
                    app.mostrar_seguranca()
                    root.update_idletasks()
                    def filhos(widget):
                        resultado = [widget]
                        for filho in widget.winfo_children():
                            resultado.extend(filhos(filho))
                        return resultado
                    itens = filhos(app.content)
                    textos = [w.cget("text") for w in itens if "text" in w.keys()]
                    self.assertTrue(any("Usuários com mais falhas: Pessoa Exemplo" in t for t in textos))
                    self.assertTrue(any("Horas com mais movimento: 10" in t for t in textos))
                    self.assertTrue(any(isinstance(w, tk.Scrollbar) for w in itens))
                    self.assertFalse(any("900100" in t for t in textos))
            finally:
                root.destroy()

    def test_base_invalida_preservada_e_aviso(self):
        with tempfile.TemporaryDirectory() as pasta:
            from pathlib import Path
            caminho = Path(pasta) / "estado.txt"
            caminho.write_text("INVALIDO\n", encoding="utf-8")
            with patch.object(interface, "PASTA", pasta), patch.object(interface.messagebox, "showerror") as aviso:
                interface.executar()
            aviso.assert_called_once()
            self.assertEqual(caminho.read_text(encoding="utf-8"), "INVALIDO\n")


if __name__ == "__main__":
    unittest.main()
