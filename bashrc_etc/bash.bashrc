# System-wide .bashrc file for interactive bash(1) shells.

# To enable the settings / commands in this file for login shells as well,
# this file has to be sourced in /etc/profile.

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, overwrite the one in /etc/profile)
PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '

# Commented out, don't overwrite xterm -T "title" -n "icontitle" by default.
# If this is an xterm set the title to user@host:dir
#case "$TERM" in
#xterm*|rxvt*)
#    PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME}: ${PWD}\007"'
#    ;;
#*)
#    ;;
#esac

# enable bash completion in interactive shells
#if ! shopt -oq posix; then
#  if [ -f /usr/share/bash-completion/bash_completion ]; then
#    . /usr/share/bash-completion/bash_completion
#  elif [ -f /etc/bash_completion ]; then
#    . /etc/bash_completion
#  fi
#fi

# sudo hint
if [ ! -e "$HOME/.sudo_as_admin_successful" ] && [ ! -e "$HOME/.hushlogin" ] ; then
    case " $(groups) " in *\ admin\ *)
    if [ -x /usr/bin/sudo ]; then
	cat <<-EOF
	To run a command as administrator (user "root"), use "sudo <command>".
	See "man sudo_root" for details.
	
	EOF
    fi
    esac
fi

# if the command-not-found package is installed, use it
if [ -x /usr/lib/command-not-found -o -x /usr/share/command-not-found/command-not-found ]; then
	function command_not_found_handle {
	        # check because c-n-f could've been removed in the meantime
                if [ -x /usr/lib/command-not-found ]; then
		   /usr/lib/command-not-found -- "$1"
                   return $?
                elif [ -x /usr/share/command-not-found/command-not-found ]; then
		   /usr/share/command-not-found/command-not-found -- "$1"
                   return $?
		else
		   printf "%s: command not found\n" "$1" >&2
		   return 127
		fi
	}
fi


# PER DISATTIVARE LA CASE SENSITIVITA DELLA SHELL VAI IN /etc/input.rc E AGGIUNGI LA LINEA
# set completion-ignore-case On

# AGGIUNGI COLORI STANDARD ALLA SHELL (non necessario in questo bash.rc)
#export LS_OPTIONS='--color=auto'
#eval "`dircolors`"
#alias ls='ls $LS_OPTIONS'

# COMPLETA SCROLLANDO CON TAB TRA LE OPZIONI
bind '"\C-i": menu-complete'

#Increase lines stored in history and unify history of multiple sessions
HISTSIZE=100000
HISTFILESIZE=1000000

#Makes unic history
export HISTCONTROL=ignoredups:erasedups                                                                 # Avoid duplicates   
shopt -s histappend                                                                                     # When the shell exits, append to the history file instead of overwriting it
export PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}history -a; history -c; history -r"       # After each command, append to the history file and reread it

#usefull path
downl="/home/carlo/Downloads/"
sou="/home/carlo/work/source/"
desktop="/mnt/windows-ssd/Documents\ and\ Settings/Sam/Desktop/"
rdrive="/mnt/R_drive/Biomolecular_Model-MANCER-HS00092/Characterization_of_molecular_interactions_of_venom_peptides_with_membranes/"

#Plumed autocomplete
_plumed() { eval "$(plumed --no-mpi completion 2>/dev/null)";}
complete -F _plumed -o default plumed


#Binary files locations
export PATH=$PATH:/scripts
export PATH=$PATH:/opt/gromacs_4.6.7/bin
export PATH=$PATH:/opt/gromacs_2018.4_plumed/bin
#export PATH=$PATH:/opt/gromacs_5.1.4/bin
export PATH=$PATH:/opt/vmd-1.9.3/
export PATH=$PATH:/opt/gromacs_rest/bin
export PATH=$PATH:/home/carlo/programs/anaconda2/bin
export PATH=$PATH:/opt/gyb

#Aliases for comands 
alias rename='rename.ul'
alias vmd='vmd-1.9.3'
alias rm='rm'
alias sourceb="source /etc/bash.bashrc"
alias delhash="rm *#* "
alias xmgrace="xmgrace -nxy "
alias cdb='cd /mnt/R_drive/Biomolecular_Model-MANCER-HS00092/Characterization_of_molecular_interactions_of_venom_peptides_with_membranes/'
alias clean="rm dhdl.xvg mdout.mdp pullf.xvg pullx.xvg state.cpt state_prev.cpt traj.xtc  traj.trr confout.gro ener.edr md.log"
alias open="xdg-open"

#USEFUL COMANDS THAT SOMETIMES IN THE PAST WORKED
# gsettings set org.gnome.desktop.wm.preferences auto-raise 'true'  # this gets rid of the "windows is ready bullshit" and instead autoopen windows when you tell ubuntu to
#
#
#
#
#
#
#
