<%doc>
 * Copyright (C) 2012-2013 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
       * Pettier Gabriel;
       * TJEBBES Gaston <g.t@majerti.fr>

 This file is part of Autonomie : Progiciel de gestion de CAE.

    Autonomie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Autonomie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
</%doc>

<%doc>
    Simple page for form rendering
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name="content">
% if info_message != UNDEFINED:
<div class="alert alert-success">
    ${info_message|n}
</div>
% endif
% if warn_message != UNDEFINED:
    <div class="alert alert-warn">
        <i class='fa fa-warning'></i>
        ${warn_message|n}
    </div>
% endif
% if help_message != UNDEFINED:
    <div class='alert alert-info'>
    <i class='fa fa-question-circle fa-2x'></i>
    ${help_message|n}
    </div>
% endif
<div class="col-md-8 col-md-offset-2">
    ${form|n}
</div>
</%block>
