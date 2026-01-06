# Neovim Setup for Initrd/Netboot Development on Kali Linux

## Purpose and Scope

This document defines the Neovim configuration for developing, debugging, and performing security analysis on diskless/netboot Linux systems, with emphasis on **emergency scenarios where graphical editors are unavailable**. Neovim is the primary tool for serial console debugging, dracut emergency shells, rescue environments, and live security patching of broken boot systems.

**Critical Use Cases**:
- Debugging initrd boot failures via serial console
- Editing files in dracut emergency shell (no persistent filesystem)
- Fixing systemd units in emergency.target rescue mode
- Security patching via SSH on headless servers
- Working inside unpacked initrd and squashfs filesystems
- tmux-based workflow for parallel serial console monitoring

---

## Installation

### Neovim 0.9+ (Required for Lua-based Configuration)

```bash
# Kali Linux typically has Neovim in repos
sudo apt update
sudo apt install neovim

# Verify version (must be 0.9+)
nvim --version

# If version is too old, install from upstream:
sudo add-apt-repository ppa:neovim-ppa/unstable
sudo apt update
sudo apt install neovim
```

### Essential Dependencies

```bash
# Language servers and linters
sudo apt install shellcheck bash-language-server python3-pip

# ripgrep and fd for fast search
sudo apt install ripgrep fd-find

# Node.js for LSP servers (if needed)
sudo apt install nodejs npm

# Tree-sitter CLI
sudo npm install -g tree-sitter-cli

# tmux for multiplexing
sudo apt install tmux
```

---

## Configuration Architecture

Neovim uses Lua for configuration. Create the following directory structure:

```
~/.config/nvim/
├── init.lua                 # Entry point
├── lua/
│   ├── options.lua         # Editor options
│   ├── keymaps.lua         # Key bindings
│   ├── plugins.lua         # Plugin management
│   └── lsp.lua             # LSP configuration
```

---

## Core Configuration Files

### init.lua

```lua
-- Entry point for Neovim configuration
require('options')
require('keymaps')
require('plugins')
require('lsp')

-- Filetype detection for initrd/systemd files
vim.filetype.add({
  extension = {
    service = 'systemd',
    socket = 'systemd',
    target = 'systemd',
    mount = 'systemd',
    path = 'systemd',
    timer = 'systemd',
    network = 'systemd',
    netdev = 'systemd',
    link = 'systemd',
    rules = 'udev',
    ipxe = 'sh',
  },
  filename = {
    ['dracut.conf'] = 'sh',
  },
  pattern = {
    ['.*/dracut/modules.d/.*/.*%.sh'] = 'sh',
    ['.*/systemd/system/.*%.service'] = 'systemd',
  },
})
```

### lua/options.lua

```lua
-- Editor behavior for systems engineering work
local opt = vim.opt

-- Display
opt.number = true
opt.relativenumber = true
opt.cursorline = true
opt.signcolumn = 'yes'
opt.colorcolumn = '80,120'
opt.wrap = false
opt.scrolloff = 8

-- Indentation (2 spaces for shell/systemd)
opt.tabstop = 2
opt.shiftwidth = 2
opt.expandtab = true
opt.smartindent = true

-- Search
opt.ignorecase = true
opt.smartcase = true
opt.hlsearch = true
opt.incsearch = true

-- Performance
opt.updatetime = 250
opt.timeoutlen = 300
opt.swapfile = false
opt.backup = false
opt.undofile = true
opt.undodir = os.getenv('HOME') .. '/.vim/undodir'

-- Splits
opt.splitbelow = true
opt.splitright = true

-- Clipboard (system integration)
opt.clipboard = 'unnamedplus'

-- Whitespace visibility
opt.list = true
opt.listchars = { tab = '» ', trail = '·', nbsp = '␣' }

-- Terminal colors
opt.termguicolors = true
```

### lua/keymaps.lua

```lua
-- Leader key
vim.g.mapleader = ' '
vim.g.maplocalleader = ' '

local keymap = vim.keymap.set

-- Essential navigation
keymap('n', '<leader>e', vim.cmd.Ex, { desc = 'File explorer' })
keymap('n', '<C-d>', '<C-d>zz', { desc = 'Scroll down (centered)' })
keymap('n', '<C-u>', '<C-u>zz', { desc = 'Scroll up (centered)' })

-- Buffer management
keymap('n', '<leader>bd', ':bd<CR>', { desc = 'Delete buffer' })
keymap('n', '<leader>bn', ':bnext<CR>', { desc = 'Next buffer' })
keymap('n', '<leader>bp', ':bprev<CR>', { desc = 'Previous buffer' })

-- Window navigation
keymap('n', '<C-h>', '<C-w>h', { desc = 'Move to left split' })
keymap('n', '<C-j>', '<C-w>j', { desc = 'Move to bottom split' })
keymap('n', '<C-k>', '<C-w>k', { desc = 'Move to top split' })
keymap('n', '<C-l>', '<C-w>l', { desc = 'Move to right split' })

-- Quick save/quit
keymap('n', '<leader>w', ':w<CR>', { desc = 'Save file' })
keymap('n', '<leader>q', ':q<CR>', { desc = 'Quit' })

-- Search and replace
keymap('n', '<leader>s', ':%s/', { desc = 'Search and replace' })
keymap('n', '<leader>nh', ':nohl<CR>', { desc = 'Clear search highlight' })

-- Systemd/initrd workflow shortcuts
keymap('n', '<leader>sv', ':!sudo systemctl daemon-reload<CR>', { desc = 'Reload systemd' })
keymap('n', '<leader>sr', ':!sudo systemctl restart %:t:r<CR>', { desc = 'Restart this service' })
keymap('n', '<leader>ss', ':!sudo systemctl status %:t:r<CR>', { desc = 'Status of this service' })
keymap('n', '<leader>sc', ':!shellcheck %<CR>', { desc = 'ShellCheck current file' })
keymap('n', '<leader>sa', ':!systemd-analyze verify %<CR>', { desc = 'Validate systemd unit' })

-- tmux integration (send command to adjacent pane)
keymap('n', '<leader>tt', ':!tmux send-keys -t :.+ "make test" C-m<CR>', { desc = 'Run test in tmux pane' })
```

### lua/plugins.lua

```lua
-- Plugin management with lazy.nvim
local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    'git',
    'clone',
    '--filter=blob:none',
    'https://github.com/folke/lazy.nvim.git',
    '--branch=stable',
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

require('lazy').setup({
  -- Color scheme
  {
    'folke/tokyonight.nvim',
    priority = 1000,
    config = function()
      vim.cmd.colorscheme('tokyonight-night')
    end,
  },

  -- Treesitter for syntax highlighting
  {
    'nvim-treesitter/nvim-treesitter',
    build = ':TSUpdate',
    config = function()
      require('nvim-treesitter.configs').setup({
        ensure_installed = { 'bash', 'lua', 'python', 'yaml', 'markdown' },
        highlight = { enable = true },
        indent = { enable = true },
      })
    end,
  },

  -- Telescope for fuzzy finding
  {
    'nvim-telescope/telescope.nvim',
    dependencies = { 'nvim-lua/plenary.nvim' },
    config = function()
      local builtin = require('telescope.builtin')
      vim.keymap.set('n', '<leader>ff', builtin.find_files, { desc = 'Find files' })
      vim.keymap.set('n', '<leader>fg', builtin.live_grep, { desc = 'Grep in files' })
      vim.keymap.set('n', '<leader>fb', builtin.buffers, { desc = 'Find buffers' })
      vim.keymap.set('n', '<leader>fh', builtin.help_tags, { desc = 'Help tags' })
    end,
  },

  -- LSP configuration
  {
    'neovim/nvim-lspconfig',
    dependencies = {
      'williamboman/mason.nvim',
      'williamboman/mason-lspconfig.nvim',
    },
  },

  -- Autocompletion
  {
    'hrsh7th/nvim-cmp',
    dependencies = {
      'hrsh7th/cmp-nvim-lsp',
      'hrsh7th/cmp-buffer',
      'hrsh7th/cmp-path',
      'L3MON4D3/LuaSnip',
    },
    config = function()
      local cmp = require('cmp')
      cmp.setup({
        snippet = {
          expand = function(args)
            require('luasnip').lsp_expand(args.body)
          end,
        },
        mapping = cmp.mapping.preset.insert({
          ['<C-b>'] = cmp.mapping.scroll_docs(-4),
          ['<C-f>'] = cmp.mapping.scroll_docs(4),
          ['<C-Space>'] = cmp.mapping.complete(),
          ['<C-e>'] = cmp.mapping.abort(),
          ['<CR>'] = cmp.mapping.confirm({ select = true }),
        }),
        sources = cmp.config.sources({
          { name = 'nvim_lsp' },
          { name = 'luasnip' },
        }, {
          { name = 'buffer' },
          { name = 'path' },
        }),
      })
    end,
  },

  -- Git integration
  {
    'lewis6991/gitsigns.nvim',
    config = function()
      require('gitsigns').setup({
        signs = {
          add = { text = '+' },
          change = { text = '~' },
          delete = { text = '_' },
          topdelete = { text = '‾' },
          changedelete = { text = '~' },
        },
      })
    end,
  },

  -- Status line
  {
    'nvim-lualine/lualine.nvim',
    dependencies = { 'nvim-tree/nvim-web-devicons' },
    config = function()
      require('lualine').setup({
        options = { theme = 'tokyonight' },
      })
    end,
  },

  -- File explorer
  {
    'nvim-tree/nvim-tree.lua',
    dependencies = { 'nvim-tree/nvim-web-devicons' },
    config = function()
      require('nvim-tree').setup()
      vim.keymap.set('n', '<leader>e', ':NvimTreeToggle<CR>', { desc = 'Toggle file tree' })
    end,
  },

  -- Comment plugin
  {
    'numToStr/Comment.nvim',
    config = function()
      require('Comment').setup()
    end,
  },

  -- Todo comments
  {
    'folke/todo-comments.nvim',
    dependencies = { 'nvim-lua/plenary.nvim' },
    config = function()
      require('todo-comments').setup({
        keywords = {
          SECURITY = { icon = '🔒', color = 'error' },
          UNSAFE = { icon = '⚠️ ', color = 'warning' },
          TODO = { icon = '✓', color = 'info' },
        },
      })
    end,
  },
})
```

### lua/lsp.lua

```lua
-- LSP configuration for shell scripts and systemd
local lspconfig = require('lspconfig')
local capabilities = require('cmp_nvim_lsp').default_capabilities()

-- Mason setup (LSP installer)
require('mason').setup()
require('mason-lspconfig').setup({
  ensure_installed = { 'bashls', 'lua_ls' },
})

-- Bash Language Server
lspconfig.bashls.setup({
  capabilities = capabilities,
  on_attach = function(client, bufnr)
    local opts = { buffer = bufnr }
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
    vim.keymap.set('n', 'K', vim.lsp.buf.hover, opts)
    vim.keymap.set('n', '<leader>rn', vim.lsp.buf.rename, opts)
    vim.keymap.set('n', '<leader>ca', vim.lsp.buf.code_action, opts)
    vim.keymap.set('n', 'gr', vim.lsp.buf.references, opts)
    vim.keymap.set('n', '<leader>f', vim.lsp.buf.format, opts)
  end,
  filetypes = { 'sh', 'bash' },
})

-- Lua Language Server (for Neovim config development)
lspconfig.lua_ls.setup({
  capabilities = capabilities,
  settings = {
    Lua = {
      diagnostics = {
        globals = { 'vim' },
      },
    },
  },
})

-- Diagnostic configuration
vim.diagnostic.config({
  virtual_text = true,
  signs = true,
  update_in_insert = false,
  underline = true,
  severity_sort = true,
  float = {
    border = 'rounded',
    source = 'always',
  },
})

-- Diagnostic signs
local signs = { Error = '✘', Warn = '▲', Hint = '⚑', Info = '' }
for type, icon in pairs(signs) do
  local hl = 'DiagnosticSign' .. type
  vim.fn.sign_define(hl, { text = icon, texthl = hl, numhl = hl })
end
```

---

## ShellCheck Integration

ShellCheck is integrated via bash-language-server (bashls), but you can also run it manually:

```bash
# In Neovim, run ShellCheck on current file
:!shellcheck %

# Or use the keymap
<leader>sc
```

For more aggressive checking, add this to your shell scripts:

```bash
# shellcheck enable=all
# shellcheck shell=bash
```

---

## Systemd Unit File Support

Neovim doesn't have native systemd syntax highlighting, but we can add it:

Create `~/.config/nvim/after/syntax/systemd.vim`:

```vim
if exists("b:current_syntax")
  finish
endif

syn match systemdComment "^#.*$"
syn match systemdSection "^\[.*\]$"
syn match systemdKey "^[A-Za-z0-9_-]\+="me=e-1
syn match systemdValue "=.*$"ms=s+1

hi def link systemdComment Comment
hi def link systemdSection Keyword
hi def link systemdKey Identifier
hi def link systemdValue String

let b:current_syntax = "systemd"
```

---

## Working Inside Unpacked Initrd and Squashfs

### Extract and Edit Initrd

```bash
# Extract initrd
mkdir ~/initrd-work
cd ~/initrd-work
lsinitrd --unpack /boot/initramfs-$(uname -r).img

# Open in Neovim
nvim .

# Navigate with Telescope
# <leader>ff to find files
# <leader>fg to grep for "network" or "mount"
```

### Mount and Edit Squashfs (Read-Only)

```bash
# Mount squashfs
sudo mkdir -p /mnt/squashfs-edit
sudo mount -o loop,ro rootfs.squashfs /mnt/squashfs-edit

# Edit files (requires copy-on-write overlay or direct copy)
sudo cp /mnt/squashfs-edit/etc/systemd/system/myservice.service ~/work/
nvim ~/work/myservice.service

# Rebuild squashfs after edits
sudo mksquashfs /path/to/rootfs ./rootfs-new.squashfs -comp xz
```

### Workflow for Live Editing Squashfs Contents

```bash
# Create overlay for editing
sudo mkdir -p /mnt/squashfs-ro /mnt/squashfs-rw /mnt/squashfs-work /mnt/squashfs-merged
sudo mount -o loop,ro rootfs.squashfs /mnt/squashfs-ro
sudo mount -t tmpfs tmpfs /mnt/squashfs-rw
sudo mkdir /mnt/squashfs-work
sudo mount -t overlay overlay -o lowerdir=/mnt/squashfs-ro,upperdir=/mnt/squashfs-rw,workdir=/mnt/squashfs-work /mnt/squashfs-merged

# Edit in merged view
cd /mnt/squashfs-merged
nvim etc/systemd/system/myservice.service

# Rebuild squashfs from merged view
sudo mksquashfs /mnt/squashfs-merged ./rootfs-patched.squashfs -comp xz
```

---

## tmux + Neovim Workflow for Serial Console Debugging

### tmux Configuration for Initrd Debugging

Create `~/.tmux.conf`:

```bash
# Prefix key (Ctrl-a instead of Ctrl-b)
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# Split panes with intuitive keys
bind | split-window -h
bind - split-window -v
unbind '"'
unbind %

# Vim-style pane navigation
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Enable mouse support
set -g mouse on

# Status bar
set -g status-style 'bg=colour235 fg=colour137'
set -g status-left '#[fg=colour197]#H '
set -g status-right '#[fg=colour81]%Y-%m-%d %H:%M'

# Start windows and panes at 1
set -g base-index 1
setw -g pane-base-index 1

# Renumber windows on close
set -g renumber-windows on

# Vi mode for copy
setw -g mode-keys vi
bind-key -T copy-mode-vi 'v' send -X begin-selection
bind-key -T copy-mode-vi 'y' send -X copy-selection-and-cancel
```

### Serial Console Debug Session Layout

```bash
# Start tmux session for debugging
tmux new-session -s initrd-debug

# Split into 3 panes:
# Top-left: Serial console output (QEMU)
# Top-right: Neovim for editing
# Bottom: Command execution

# Layout commands:
Ctrl-a %    # Split vertically
Ctrl-a "    # Split horizontally

# Example session:
# Pane 1 (top-left): qemu-system-x86_64 -serial stdio ...
# Pane 2 (top-right): nvim ~/initrd-work/usr/lib/dracut/modules.d/90network/ifup.sh
# Pane 3 (bottom): watch -n1 'systemctl status'
```

### Real-World Debugging Workflow

```bash
# Terminal 1: Start QEMU with serial console
tmux new -s debug
qemu-system-x86_64 -m 2048 -kernel /boot/vmlinuz -initrd /boot/initramfs.img \
  -append "console=ttyS0 rd.break=pre-mount rd.debug" \
  -serial stdio -nographic

# Terminal 2 (tmux pane): Edit initrd scripts
Ctrl-a |  # Split vertically
cd ~/initrd-work
nvim usr/lib/dracut/modules.d/90network/net-lib.sh

# Make fix, save, rebuild initrd
:w
:!sudo dracut --force /boot/initramfs-test.img

# Terminal 3 (tmux pane): Monitor logs
Ctrl-a -  # Split horizontally
tail -f /var/log/dracut.log

# Switch between panes with Ctrl-a h/j/k/l
```

---

## Why Neovim is Critical for Early Boot Debugging

### Scenarios Where VS Code Cannot Be Used

| Scenario | Why VS Code Fails | Neovim Solution |
|----------|-------------------|-----------------|
| **Dracut emergency shell** | No GUI, limited `vi` available | Neovim works in any terminal |
| **Serial console (QEMU/IPMI)** | No X11 forwarding, text-only | Neovim in tmux over serial |
| **Broken initrd (rd.break)** | Boot stops before GUI starts | Edit scripts in emergency shell |
| **SSH to headless server** | No display server | Neovim via SSH |
| **emergency.target rescue** | systemd failed, no GUI | Fix units in rescue shell |
| **Live ISO rescue environment** | May lack GUI packages | Neovim in live environment |

### Emergency Boot Fixing Workflow

```bash
# Boot fails, dropped to dracut emergency shell
# Kernel cmdline: rd.break=pre-mount

# Mount root filesystem manually
mount -t proc proc /proc
mount -t sysfs sys /sys
mount -t devtmpfs dev /dev

# Check what's available
which vi nvim nano

# Edit the broken script (vi is always available, but limited)
vi /usr/lib/dracut/modules.d/90network/ifup.sh

# Or if Neovim was included in initrd:
nvim /usr/lib/dracut/modules.d/90network/ifup.sh

# Fix the issue, exit shell to continue boot
exit
```

### Including Neovim in Custom Initrd

If you need Neovim in emergency scenarios, add it to dracut:

```bash
# Create dracut module for Neovim
sudo mkdir -p /usr/lib/dracut/modules.d/99nvim
sudo tee /usr/lib/dracut/modules.d/99nvim/module-setup.sh << 'EOF'
#!/bin/bash
check() { return 0; }
depends() { return 0; }
install() {
    inst_binary nvim
    inst_simple /usr/share/nvim/runtime/syntax/sh.vim
}
EOF
sudo chmod +x /usr/lib/dracut/modules.d/99nvim/module-setup.sh

# Rebuild initrd with Neovim included
sudo dracut --force --add nvim /boot/initramfs-rescue.img
```

---

## Live Security Patching in Broken Boot Environments

### Scenario: CVE in initrd network script

```bash
# Boot into rescue mode
systemctl rescue

# Or from GRUB, add to kernel cmdline:
# systemd.unit=rescue.target

# Extract current initrd
mkdir /tmp/initrd-patch
cd /tmp/initrd-patch
lsinitrd --unpack /boot/initramfs-$(uname -r).img

# Open vulnerable script in Neovim
nvim usr/lib/dracut/modules.d/40network/net-lib.sh

# Find vulnerable function (e.g., unquoted variable)
# Before:
#   ip link set $iface up
# After:
#   ip link set "${iface}" up

# Validate fix with ShellCheck
:!shellcheck %

# Rebuild initrd from patched directory
cd /tmp/initrd-patch
find . | cpio -o -H newc | gzip > /boot/initramfs-patched.img

# Update GRUB to use patched initrd
sudo grubby --update-kernel=ALL --args="initrd=/boot/initramfs-patched.img"

# Reboot to test
reboot
```

### Security Review Workflow in Neovim

```bash
# Open all shell scripts in initrd
nvim ~/initrd-work

# Search for security issues with Telescope
<leader>fg
# Search for: "eval", "password", "unquoted", "curl.*http://"

# Use Todo-Comments to mark issues
# In a script, add:
# SECURITY: This variable is not quoted
ip link set $iface up

# Find all security markers
:TodoTelescope keywords=SECURITY,UNSAFE

# Batch fix with substitution
:%s/\$iface/"${iface}"/gc
```

---

## Command-Line Tools Integration

### Quick Scripts for Common Tasks

Add these to `~/bin/` and add to PATH:

```bash
# ~/bin/initrd-edit
#!/bin/bash
INITRD=${1:-/boot/initramfs-$(uname -r).img}
WORKDIR=~/initrd-work-$(date +%s)
mkdir -p "$WORKDIR"
cd "$WORKDIR" || exit
lsinitrd --unpack "$INITRD"
nvim .
echo "Rebuild with: cd $WORKDIR && find . | cpio -o -H newc | gzip > /boot/initramfs-new.img"
```

```bash
# ~/bin/squashfs-edit
#!/bin/bash
SQUASHFS=${1:-./rootfs.squashfs}
MOUNT=/mnt/squashfs-edit-$$
sudo mkdir -p "$MOUNT"
sudo mount -o loop,ro "$SQUASHFS" "$MOUNT"
cd "$MOUNT" || exit
nvim .
echo "Remember to rebuild squashfs after editing"
```

---

## Performance Optimization for Large Initrd/Squashfs

### Neovim Performance Tuning

Add to `lua/options.lua`:

```lua
-- Optimize for large files (initrd can be 100+ MB unpacked)
opt.swapfile = false
opt.backup = false
opt.writebackup = false

-- Faster grep with ripgrep
if vim.fn.executable('rg') == 1 then
  opt.grepprg = 'rg --vimgrep --no-heading --smart-case'
  opt.grepformat = '%f:%l:%c:%m,%f:%l:%m'
end

-- Exclude binary files from search
opt.wildignore = '*.o,*.obj,*.bin,*.img,*.squashfs,*.cpio,*.gz'
```

### Telescope Configuration for Faster Search

Add to Telescope setup in `lua/plugins.lua`:

```lua
require('telescope').setup({
  defaults = {
    file_ignore_patterns = {
      "%.squashfs$",
      "%.cpio$",
      "%.img$",
      "%.o$",
      "%.bin$",
      "node_modules/",
    },
    vimgrep_arguments = {
      'rg',
      '--color=never',
      '--no-heading',
      '--with-filename',
      '--line-number',
      '--column',
      '--smart-case',
      '--hidden',
      '--glob=!.git/',
    },
  },
})
```

---

## Minimal Neovim for Rescue Environments

If you need a stripped-down Neovim config for emergency use (e.g., on a minimal rescue ISO), use this single-file configuration:

```lua
-- Minimal init.lua for rescue environments
vim.opt.number = true
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true
vim.g.mapleader = ' '

-- Essential keymaps
vim.keymap.set('n', '<leader>w', ':w<CR>')
vim.keymap.set('n', '<leader>q', ':q<CR>')
vim.keymap.set('n', '<leader>sc', ':!shellcheck %<CR>')

-- Syntax highlighting (built-in)
vim.cmd('syntax on')
vim.cmd('filetype plugin indent on')
```

Save as `~/.config/nvim/init-minimal.lua` and use with:

```bash
nvim -u ~/.config/nvim/init-minimal.lua
```

---

## Comparison: Neovim vs. VS Code for Initrd Work

| Task | VS Code | Neovim |
|------|---------|--------|
| **Development (workstation)** | ✓ Excellent (full IDE) | ✓ Excellent (fast, extensible) |
| **Serial console debugging** | ✗ Cannot use | ✓ Perfect fit |
| **Dracut emergency shell** | ✗ No GUI | ✓ Works with vi fallback |
| **SSH to headless server** | ~ Possible but slow | ✓ Native environment |
| **tmux integration** | ✗ Not designed for it | ✓ Designed for multiplexing |
| **Large file performance** | ~ Can be slow | ✓ Fast on any size |
| **Rescue ISO/live environment** | ✗ Usually not available | ✓ vi/nvim always available |
| **Broken systemd debugging** | ✗ Cannot start GUI | ✓ Works in emergency.target |
| **Learning curve** | Easy | Moderate (modal editing) |

**Conclusion**: Use VS Code for comfortable development, Neovim for everything else, especially debugging and emergency response.

---

## Final Workflow Integration

### Daily Development Cycle

1. **Morning**: VS Code for structured development and security review tasks
2. **QEMU testing**: tmux + Neovim for serial console monitoring
3. **Debug failures**: Neovim inside unpacked initrd
4. **Emergency fixes**: Neovim in rescue shell or via SSH

### Muscle Memory Development

To become proficient with Neovim for emergency scenarios, practice these workflows weekly:

```bash
# Practice 1: Edit initrd under time pressure
time initrd-edit /boot/initramfs-$(uname -r).img

# Practice 2: Fix script in tmux while monitoring serial console
tmux new -s practice
# (setup 3-pane layout as described above)

# Practice 3: Work without LSP/plugins (simulate rescue environment)
nvim -u NONE broken-script.sh
```

---

## Security-Specific Workflows

### Audit All Initrd Scripts for Vulnerabilities

```bash
# Extract initrd
cd ~/initrd-audit
lsinitrd --unpack /boot/initramfs-$(uname -r).img

# Open Neovim
nvim .

# Search for common vulnerability patterns
:Telescope live_grep
# Search terms:
#   eval
#   source /tmp
#   curl.*http://
#   password
#   token
#   unquoted.*\$

# Mark findings with TODO comments
# SECURITY: Unquoted variable expansion
# UNSAFE: Evaluating user input
# CVE-XXXX-YYYY: Affected by known vulnerability
```

### Patch Workflow for Zero-Day in Boot Component

```bash
# 1. Receive CVE notification
# 2. Extract affected initrd
initrd-edit /boot/initramfs-$(uname -r).img

# 3. Locate vulnerable code in Neovim
<leader>fg  # Search for affected function

# 4. Apply patch
# (manual edit or :r !curl https://patch-url)

# 5. Validate with ShellCheck
<leader>sc

# 6. Rebuild initrd
cd ~/initrd-work-*
find . | cpio -o -H newc | gzip > /boot/initramfs-patched.img

# 7. Test in QEMU with tmux monitoring
tmux new -s cve-test
qemu-system-x86_64 -kernel /boot/vmlinuz -initrd /boot/initramfs-patched.img -serial stdio

# 8. Deploy to production if test passes
sudo cp /boot/initramfs-patched.img /boot/initramfs-$(uname -r).img
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

---

## Conclusion

Neovim is the **essential tool** for initrd and netboot systems work because it functions in every environment where debugging and fixing must occur: serial consoles, rescue shells, SSH sessions, and broken boot scenarios. While VS Code provides a superior development experience for structured work, Neovim is irreplaceable when systems fail and immediate fixes are required.

**Key Takeaway**: Master Neovim for emergency response. Your ability to quickly edit scripts in a dracut emergency shell or systemd rescue target will determine whether a system boots or remains down.

For development comfort, use VS Code. For production resilience and security incident response, rely on Neovim.
