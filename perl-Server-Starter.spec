#
# Conditional build:
%bcond_without	tests		# do not perform "make test"

%define		pdir	Server
%define		pnam	Starter
%include	/usr/lib/rpm/macros.perl
Summary:	Server::Starter - a superdaemon for hot-deploying server programs
Name:		perl-Server-Starter
Version:	0.11
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Server/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	037d75831a23ca76cd306d678b20332e
URL:		http://search.cpan.org/dist/Server-Starter/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-List-MoreUtils
BuildRequires:	perl-Proc-Wait3
BuildRequires:	perl-Scope-Guard
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
It is often a pain to write a server program that supports graceful
restarts, with no resource leaks. Server::Starter, solves the problem
by splitting the task into two. One is start_server, a script provided
as a part of the module, which works as a superdaemon that binds to
zero or more TCP ports or unix sockets, and repeatedly spawns the
server program that actually handles the necessary tasks (for example,
responding to incoming commenctions). The spawned server programs
under Server::Starter call accept(2) and handle the requests.

To gracefully restart the server program, send SIGHUP to the
superdaemon. The superdaemon spawns a new server program, and if (and
only if) it starts up successfully, sends SIGTERM to the old server
program.

By using Server::Starter it is much easier to write a hot-deployable
server. Following are the only requirements a server program to be run
under Server::Starter should conform to:

- receive file descriptors to listen to through an environment
  variable
- perform a graceful shutdown when receiving SIGTERM

A Net::Server personality that can be run under Server::Starter exists
under the name Net::Server::SS::PreFork.



# %description -l pl.UTF-8 # TODO

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%attr(755,root,root) %{_bindir}/start_server
%{_mandir}/man1/start_server.1p*
%{perl_vendorlib}/Server/*.pm
%{_mandir}/man3/*
