{ ... }:
{
  # https://devenv.sh/basics/
  env = {
    UV_PYTHON_DOWNLOADS = "never";
  };

  # https://devenv.sh/packages/
  packages = [ ];

  # https://devenv.sh/languages/
  languages.python = {
    enable = true;
    venv.enable = true;
    uv.enable = true;
    uv.sync.enable = true;
  };

  # https://devenv.sh/scripts/

  # https://devenv.sh/tasks/

  # https://devenv.sh/git-hooks/
  pre-commit.default_stages = [
    "pre-push"
    "manual"
  ];
  pre-commit.hooks = {
    ruff.enable = true;
    ruff-format.enable = true;
    check-added-large-files.enable = true;
    check-json.enable = true;
    check-toml.enable = true;
    check-yaml.enable = true;
    trim-trailing-whitespace = {
      enable = true;
      excludes = [ ".*.md$" "xml/" ];
    };
    end-of-file-fixer.enable = true;
  };

  # See full reference at https://devenv.sh/reference/options/
}
